from typing import Annotated

from fastapi import APIRouter, Query

from app.deps import SessionDep
from app.schemas import User
from app.services.user_service import create_user as create_user_service

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/create-user/')
async def create_user(*, session: SessionDep, user: Annotated[User, Query()]):
    # if exists: raise UserExistsError
    create_user_service(session, user)
    return {'result': 'ok'}
