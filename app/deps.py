import os
from typing import Annotated, Generator

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

load_dotenv()

POSTGRES_URI = (
    # postgresql://[user[:password]@]host[:port][/dbname][?param1=value1&param2=value2]
    f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}'
    f'@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}'
    f'/{os.getenv("POSTGRES_DB")}'
)

# todo: move to `config.py`
engine = create_engine(POSTGRES_URI, echo=True)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
