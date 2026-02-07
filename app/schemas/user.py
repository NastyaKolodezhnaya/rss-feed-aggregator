from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str  # todo: validate email
    password: str
