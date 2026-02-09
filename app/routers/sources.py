from fastapi import APIRouter

from app.deps import SessionDep
from app.schemas import AddSourceRequest
from app.services.source_service import create_source, source_exists
from app.services.user_service import add_new_user_source, get_user

router = APIRouter(prefix='/sources', tags=['sources'])


@router.post('/add')
def add_new_source(*, session: SessionDep, request: AddSourceRequest):
    # assert user exists
    user = get_user(session, request.user_id)
    if not user:
        raise ValueError  # todo: raise it properly

    existing = source_exists(session, request.feed_link)
    if not existing:
        existing = create_source(session, request.feed_link)

    add_new_user_source(user, existing)
    return {'result': 'ok'}  # todo: make valid responses
