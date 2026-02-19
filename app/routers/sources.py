from fastapi import APIRouter

from app.deps import SessionDep, UserDep
from app.services.source_service import add_new_source, delete_source_by_id, source_exists
from app.services.user_service import add_new_user_source, convert_user_db_from_request

router = APIRouter(prefix='/sources', tags=['sources'], dependencies=[UserDep])


@router.post('/add')
def add_source(*, session: SessionDep, user: UserDep, feed_link: str):
    existing = source_exists(session, feed_link)
    if not existing:
        existing = add_new_source(session, feed_link)

    add_new_user_source(session, user, existing)
    return {'result': 'ok'}  # todo: make valid responses


@router.get('/list')
def get_sources_by_user(*, user: UserDep):
    user_db = convert_user_db_from_request(user)
    return {'sources': user_db.sources}


@router.get('/{source_id}')
def get_source(*, session: SessionDep, source_id: int):
    return {'source': get_source(session, source_id)}
    # todo: return SourceNotExistError


@router.delete('/{source_id}')
def delete_source(*, session: SessionDep, source_id: int):
    delete_source_by_id(session, source_id)
    return {'result': 'ok'}
    # todo: return SourceNotExistError
