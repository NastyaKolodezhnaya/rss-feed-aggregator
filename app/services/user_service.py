from sqlalchemy import select

from app.models import Source as Source_Db
from app.models import User as User_Db
from app.schemas import User as User_Create
from app.utils.hash import get_hashed_password


def create_user(session, user_create: User_Create) -> User_Db:
    hash_pass = get_hashed_password(user_create.password)  # todo: move to frontend
    db_user = User_Db(name=user_create.name, email=user_create.email, password_hash=hash_pass)

    session.add(db_user)
    session.commit()
    return db_user


def get_user_by_id(session, user_id: int) -> User_Db:
    stmt = select(User_Db).where(User_Db.id == user_id)
    result = session.execute(stmt)
    return result.scalars().first()


def add_new_user_source(session, user: User_Db, source_db: Source_Db):
    user.sources.append(source_db)
    session.commit()
