import os
from typing import Annotated, Generator

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Request
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.schemas import User
from app.services.user_service import get_user_by_id

load_dotenv()

POSTGRES_URI = (
    # postgresql://[user[:password]@]host[:port][/dbname][?param1=value1&param2=value2]
    f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}'
    f'@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}'
    f'/{os.getenv("POSTGRES_DB")}'
)

engine = create_engine(POSTGRES_URI, echo=True)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


def get_current_user_session(request: Request, db_session: Session = SessionDep):
    user_id = request.session.get('user_id')
    if not user_id:
        raise HTTPException(status_code=401)
    user_db = get_user_by_id(db_session, user_id)
    return User.model_validate(user_db)


UserDep = Annotated[User, Depends(get_current_user_session)]
