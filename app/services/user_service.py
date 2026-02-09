from app.models import User as User_Db
from app.schemas import User as User_Create
from app.utils.hash import get_hashed_password


def create_user(session, user_create: User_Create):
    hash_pass = get_hashed_password(user_create.password)  # todo: move to frontend
    db_user = User_Db(name=user_create.name, email=user_create.email, password_hash=hash_pass)

    session.add(db_user)
    session.commit()
