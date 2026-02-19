from fastapi import APIRouter, HTTPException

from app.deps import SessionDepType, UserDep, UserDepType
from app.schemas import EntryBrief, EntryBriefListResponse, EntryListResponse, EntryResponse
from app.services.entry_service import add_new_entries, get_all_user_entries, get_entry_by_id
from app.services.source_service import get_source_by_id
from app.utils.parse import parse_feed

router = APIRouter(prefix='/entries', tags=['entries'], dependencies=[UserDep])


@router.get('/fetch/{source_id}', response_model=EntryListResponse)
def fetch_entries(*, session: SessionDepType, source_id: int):
    src = get_source_by_id(session, source_id)
    if not src:
        raise HTTPException(status_code=404, detail='Source not found.')

    new_entries = parse_feed(src.feed_link, src.last_etag, src.last_modified)
    if new_entries:
        add_new_entries(session, new_entries)
    return {'entries': new_entries or []}


@router.get('/source/{source_id}', response_model=EntryListResponse)
def get_entries_by_source(*, session: SessionDepType, source_id: int):
    src = get_source_by_id(session, source_id)
    if not src:
        raise HTTPException(status_code=404, detail='Source not found.')
    return {'entries': src.entries}


@router.get('/detail/{entry_id}', response_model=EntryResponse)
def get_entry(*, session: SessionDepType, entry_id: int):
    entry = get_entry_by_id(session, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail='Entry not found.')
    return {'entry': entry}


@router.get('/list/{n}', response_model=EntryBriefListResponse)
def list_entries(*, session: SessionDepType, user: UserDepType, n: int):
    if n <= 0:
        raise HTTPException(status_code=422, detail='Number of entries must be positive.')
    rows = get_all_user_entries(session, user, n)
    return {'entries': [EntryBrief.model_validate(row) for row in rows]}
