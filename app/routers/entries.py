from fastapi import APIRouter, HTTPException, Request

from app.deps import SessionDepType, UserDep, UserDepType
from app.schemas import EntryBrief
from app.services.entry_service import add_new_entries, get_all_user_entries, get_entry_by_id
from app.services.source_service import get_source_by_id
from app.template import templates
from app.utils.parse import parse_feed

router = APIRouter(prefix='/entries', tags=['entries'], dependencies=[UserDep])


@router.get('/fetch/{source_id}')
def fetch_entries(*, request: Request, session: SessionDepType, source_id: int):
    src = get_source_by_id(session, source_id)
    if not src:
        raise HTTPException(status_code=404, detail='Source not found.')

    new_entries = parse_feed(src.feed_link, src.last_etag, src.last_modified)
    if new_entries:
        add_new_entries(session, new_entries)

    entries = src.entries
    return templates.TemplateResponse(request, 'partials/entry_list.html', {'entries': entries})


@router.get('/source/{source_id}')
def get_entries_by_source(*, request: Request, session: SessionDepType, source_id: int):
    src = get_source_by_id(session, source_id)
    if not src:
        raise HTTPException(status_code=404, detail='Source not found.')
    return templates.TemplateResponse(request, 'partials/entry_list.html', {'entries': src.entries})


@router.get('/detail/{entry_id}')
def get_entry(*, request: Request, session: SessionDepType, entry_id: int):
    entry = get_entry_by_id(session, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail='Entry not found.')
    return templates.TemplateResponse(request, 'entry_detail.html', {'entry': entry})


@router.get('/list/{n}')
def list_entries(*, request: Request, session: SessionDepType, user: UserDepType, n: int):
    if n <= 0:
        raise HTTPException(status_code=422, detail='Number of entries must be positive.')
    rows = get_all_user_entries(session, user, n)
    entries = [EntryBrief.model_validate(row) for row in rows]
    return templates.TemplateResponse(request, 'feed.html', {'entries': entries})
