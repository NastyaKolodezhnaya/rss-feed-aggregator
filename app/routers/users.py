from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Request

from app.deps import SessionDep
from app.schemas import AuthFormRequest, User
from app.services.user_service import create_user as create_user_service
from app.services.user_service import verify_user

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/signup/')
def signup(*, session: SessionDep, user: Annotated[User, Query()]):
    # if exists: raise UserExistsError
    create_user_service(session, user)
    return {'result': 'ok'}


@router.post('/login')
def login(request: Request, form_data: AuthFormRequest, session: SessionDep):
    user = verify_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401)  # not exists or password failed

    request.session['user_id'] = user.id
    return {'result': 'ok'}


@router.post('/logout')
def logout(request: Request):
    request.session.clear()
    return {'result': 'ok'}
