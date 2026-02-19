from sqlalchemy import select

from app.models import Source as Source_Db
from app.models import User as User_Db
from app.schemas import User as User_Create
from app.utils.hash import check_password, get_hashed_password


def create_user(session, user_create: User_Create) -> User_Db:
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
    stmt = select(User_Db).where(User_Db.name == username)
    result = session.execute(stmt)
    return result.scalars().first()


def add_new_user_source(session, user_id: int, source_db: Source_Db):
    user_db = get_user_by_id(session, user_id)
    user_db.sources.append(source_db)
    session.commit()


def verify_user(session, username: str, password: str) -> User_Db | None:
    user = get_user_by_name(session, username)
    if not user:
        return None

    if not check_password(password, user.password_hash):
        return None

    return user
