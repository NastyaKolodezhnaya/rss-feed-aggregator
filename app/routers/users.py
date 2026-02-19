from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Request
from sqlalchemy.exc import IntegrityError

from app.deps import SessionDepType, UserDep
from app.schemas import AuthFormRequest, UserCreate
from app.services.user_service import create_user as create_user_service
from app.services.user_service import verify_user

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/signup/')
def signup(*, session: SessionDepType, user: Annotated[UserCreate, Query()]):
    try:
        create_user_service(session, user)
    except IntegrityError:
        raise HTTPException(status_code=409, detail='Username or email already taken.')
    return {'result': 'ok'}


@router.post('/login')
def login(request: Request, session: SessionDepType, form_data: AuthFormRequest):
    user = verify_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid username or password.')

    request.session['user_id'] = user.id
    return {'result': 'ok'}


@router.post('/logout', dependencies=[UserDep])
def logout(request: Request):
    request.session.clear()
    return {'result': 'ok'}
