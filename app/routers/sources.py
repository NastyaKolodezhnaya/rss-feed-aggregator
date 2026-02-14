from fastapi import APIRouter

from app.deps import SessionDep
from app.schemas import AddSourceRequest
from app.services.source_service import add_new_source, delete_source_by_id, source_exists
from app.services.user_service import add_new_user_source, get_user_by_id

router = APIRouter(prefix='/sources', tags=['sources'])


@router.post('/add')
def add_source(*, session: SessionDep, request: AddSourceRequest):
    # assert user exists
    user = get_user_by_id(session, request.user_id)
    if not user:
        raise ValueError  # todo: raise it properly

    existing = source_exists(session, request.feed_link)
    if not existing:
        existing = add_new_source(session, request.feed_link)

    add_new_user_source(session, user, existing)
    return {'result': 'ok'}  # todo: make valid responses


@router.get('/{user_id}')
def get_sources_by_user(*, session: SessionDep, user_id: int):
    user = get_user_by_id(session, user_id)
    return {'sources': user.sources}


@router.get('/{source_id}')
def get_source(*, session: SessionDep, source_id: int):
    return {'source': get_source(session, source_id)}
    # todo: return SourceNotExistError


@router.delete('/{source_id}')
def delete_source(*, session: SessionDep, source_id: int):
    delete_source_by_id(session, source_id)
    return {'result': 'ok'}
    # todo: return SourceNotExistError
