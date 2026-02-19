from fastapi import APIRouter

from app.deps import SessionDep, UserDep
from app.services.entry_service import add_new_entries, get_all_user_entries, get_entry_by_id
from app.services.source_service import get_source_by_id
from app.utils.parse import parse_feed

router = APIRouter(prefix='/entries', tags=['entries'], dependencies=[UserDep])


@router.get('/fetch/{source_id}')
def fetch_entries(*, session: SessionDep, source_id: int):
    src = get_source_by_id(session, source_id)
    new_entries = parse_feed(src.feed_link, src.last_etag, src.last_modified)
    if new_entries:
        add_new_entries(session, new_entries)
    return {'entries': new_entries}


@router.get('/get/{source_id}')
def get_entries(*, session: SessionDep, source_id: int):
    src = get_source_by_id(session, source_id)
    return {'entries': src.entries}


@router.get('/get/{entry_id}')
def get_entry(*, session: SessionDep, entry_id: int):
    return {'entry': get_entry_by_id(session, entry_id)}


@router.get('/list/{n}')
def list_entries(*, session: SessionDep, user: UserDep, n: int):
    return {'entries': get_all_user_entries(session, user, n)}
