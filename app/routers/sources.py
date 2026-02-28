from fastapi import APIRouter, Form, HTTPException, Request, Response

from app.deps import SessionDepType, UserDep, UserDepType
from app.services.source_service import add_new_source, get_source_by_id, remove_source_if_orphaned, source_exists
from app.services.user_service import add_new_user_source, get_user_by_id, unsubscribe_user_from_source
from app.template import templates

router = APIRouter(prefix='/sources', tags=['sources'], dependencies=[UserDep])


@router.post('/add')
def add_source(*, request: Request, session: SessionDepType, user: UserDepType, feed_link: str = Form()):
    existing = source_exists(session, feed_link)
    if not existing:
        existing = add_new_source(session, feed_link)
        if not existing:
            raise HTTPException(status_code=422, detail='Failed to parse the feed. Check the URL and try again.')

    add_new_user_source(session, user.id, existing)
    user_db = get_user_by_id(session, user.id)
    return templates.TemplateResponse(request, 'partials/source_list.html', {'sources': user_db.sources})


@router.get('/list')
def get_sources_by_user(*, request: Request, session: SessionDepType, user: UserDepType):
    user_db = get_user_by_id(session, user.id)
    return templates.TemplateResponse(request, 'sources.html', {'sources': user_db.sources})


@router.get('/{source_id}')
def get_source(*, request: Request, session: SessionDepType, source_id: int):
    source = get_source_by_id(session, source_id)
    if not source:
        raise HTTPException(status_code=404, detail='Source not found.')
    return templates.TemplateResponse(request, 'source_detail.html', {'source': source, 'entries': source.entries})


@router.delete('/delete/{source_id}')
def delete_source(*, session: SessionDepType, user: UserDepType, source_id: int):
    removed = unsubscribe_user_from_source(session, user.id, source_id)
    if not removed:
        raise HTTPException(status_code=404, detail='Source not found.')
    remove_source_if_orphaned(session, removed)
    return Response(status_code=200)
