from fastapi import APIRouter, HTTPException

from app.deps import SessionDep, UserDep
from app.schemas import SourceListResponse, SourceResponse
from app.services.source_service import add_new_source, delete_source_by_id, get_source_by_id, source_exists
from app.services.user_service import add_new_user_source, get_user_by_id

router = APIRouter(prefix='/sources', tags=['sources'], dependencies=[UserDep])


@router.post('/add')
def add_source(*, session: SessionDep, user: UserDep, feed_link: str):
    existing = source_exists(session, feed_link)
    if not existing:
        existing = add_new_source(session, feed_link)
        if not existing:
            raise HTTPException(status_code=422, detail='Failed to parse the feed. Check the URL and try again.')

    add_new_user_source(session, user.id, existing)
    return {'result': 'ok'}


@router.get('/list', response_model=SourceListResponse)
def get_sources_by_user(*, session: SessionDep, user: UserDep):
    user_db = get_user_by_id(session, user.id)
    return {'sources': user_db.sources}


@router.get('/{source_id}', response_model=SourceResponse)
def get_source(*, session: SessionDep, source_id: int):
    source = get_source_by_id(session, source_id)
    if not source:
        raise HTTPException(status_code=404, detail='Source not found.')
    return {'source': source}


@router.delete('/delete/{source_id}')
def delete_source(*, session: SessionDep, source_id: int):
    deleted = delete_source_by_id(session, source_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Source not found.')
    return {'result': 'ok'}
