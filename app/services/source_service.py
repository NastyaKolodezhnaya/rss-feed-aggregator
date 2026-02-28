from dataclasses import asdict

from sqlalchemy import delete, select

from app.models import Entry as Entry_Db
from app.models import Source as Source_Db
from app.services.entry_service import add_new_entries
from app.utils.parse import ParsedSource, construct_new_feed


def source_exists(session, feed_link: str) -> Source_Db | None:
    stmt = select(Source_Db).where(Source_Db.feed_link == feed_link)
    result = session.execute(stmt)
    return result.scalars().first() or None


def add_new_source(session, feed_link: str) -> Source_Db | None:
    source_data = construct_new_feed(feed_link)

    if not isinstance(source_data, ParsedSource):
        return None

    if existing_source_db := source_exists(session, source_data.feed_link):
        add_new_entries(session, existing_source_db.entries)
        return existing_source_db

    source_kwargs = asdict(source_data)
    entries_kwargs = source_kwargs.pop('entries')

    source_db = Source_Db(**source_kwargs, entries=[Entry_Db(**e) for e in entries_kwargs])

    session.add(source_db)
    session.commit()
    return source_db


def get_source_by_id(session, source_id: int) -> Source_Db | None:
    stmt = select(Source_Db).where(Source_Db.id == source_id)
    result = session.execute(stmt)
    return result.scalars().first() or None


def delete_source_by_id(session, source_id: int) -> bool:
    source = get_source_by_id(session, source_id)
    if not source:
        return False
    stmt = delete(Source_Db).where(Source_Db.id == source_id)
    session.execute(stmt)
    session.commit()
    return True


def remove_source_if_orphaned(session, source_db: Source_Db) -> bool:
    if not source_db.users:
        return delete_source_by_id(session, source_db.id)
    return False
