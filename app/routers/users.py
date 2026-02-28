from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import IntegrityError

from app.deps import SessionDepType, UserDep
from app.schemas import UserCreate
from app.services.user_service import create_user as create_user_service
from app.services.user_service import verify_user
from app.template import templates

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/login')
def login_page(request: Request):
    return templates.TemplateResponse(request, 'login.html')


@router.get('/signup')
def signup_page(request: Request):
    return templates.TemplateResponse(request, 'signup.html')


@router.post('/signup')
def signup(
    *, request: Request, session: SessionDepType, username: str = Form(), email: str = Form(), password: str = Form()
):
    try:
        user = UserCreate(username=username, email=email, password=password)
        create_user_service(session, user)
    except IntegrityError:
        return templates.TemplateResponse(request, 'signup.html', {'error': 'Username or email already taken.'})
    except Exception:
        return templates.TemplateResponse(
            request, 'signup.html', {'error': 'Invalid input. Password must be at least 8 characters.'}
        )
    return RedirectResponse('/users/login', status_code=303)


@router.post('/login')
def login(*, request: Request, session: SessionDepType, username: str = Form(), password: str = Form()):
    user = verify_user(session, username, password)
    if not user:
        return templates.TemplateResponse(request, 'login.html', {'error': 'Invalid username or password.'})

    request.session['user_id'] = user.id
    return RedirectResponse('/entries/list', status_code=303)


@router.post('/logout', dependencies=[UserDep])
def logout(request: Request):
    request.session.clear()
    return RedirectResponse('/users/login', status_code=303)
