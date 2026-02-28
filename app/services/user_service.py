import logging

from sqlalchemy import select

from app.models import Source as Source_Db
from app.models import User as User_Db
from app.schemas import UserCreate
from app.utils.hash import check_password, get_hashed_password

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def create_user(session, user_create: UserCreate) -> User_Db:
    hash_pass = get_hashed_password(user_create.password)  # todo: move to frontend
    db_user = User_Db(username=user_create.username, email=user_create.email, password_hash=hash_pass)

    session.add(db_user)
    session.commit()
    return db_user


def get_user_by_id(session, user_id: int) -> User_Db | None:
    stmt = select(User_Db).where(User_Db.id == user_id)
    result = session.execute(stmt)
    return result.scalars().first()


def get_user_by_name(session, username: str) -> User_Db | None:
    stmt = select(User_Db).where(User_Db.username == username)
    result = session.execute(stmt)
    return result.scalars().first()


def add_new_user_source(session, user_id: int, source_db: Source_Db):
    user_db = get_user_by_id(session, user_id)
    user_db.sources.append(source_db)
    session.commit()


def unsubscribe_user_from_source(session, user_id: int, source_id: int) -> Source_Db | bool:
    user_db = get_user_by_id(session, user_id)
    if not user_db:
        return False
    source: Source_Db = next((s for s in user_db.sources if s.id == source_id), None)
    if not source:
        return False
    user_db.sources.remove(source)
    session.commit()
    return source


def verify_user(session, username: str, password: str) -> User_Db | None:
    user = get_user_by_name(session, username)
    logger.info(f'searching for user with {username=}')
    if not user:
        return None

    logger.info(f'found user with {username=}: {user}. verifying the password...')
    if not check_password(password, user.password_hash):
        logger.warning(f'password for {user=} is incorrect')
        return None

    return user
