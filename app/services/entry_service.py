from dataclasses import asdict

from sqlalchemy.sql.expression import select

from app.models import Entry as Entry_Db
from app.models import Source as Source_Db
from app.models import user_to_source
from app.schemas import User
from app.utils.parse import ParsedEntry


def entry_exists(session, entry_link: str):
    stmt = select(Entry_Db).where(Entry_Db.link == entry_link)
    result = session.execute(stmt)
    return result.scalars().first() or None


def add_new_entries(session, entries: list[ParsedEntry]):
    final_entries = []
    for entry in entries:
        if entry_exists(session, entry.link):
            final_entries.append(entry)
            continue

        entries_kwargs = asdict(entry)
        entry_db = Entry_Db(**entries_kwargs)

        session.add(entry_db)
        final_entries.append(entry_db)

    session.commit()
    return final_entries


def get_entry_by_id(session, entry_id: int) -> Entry_Db | None:
    stmt = select(Entry_Db).where(Entry_Db.id == entry_id)
    result = session.execute(stmt).scalar()
    return result or None


def get_all_user_entries(session, user: User, limit: int, offset: int = 0):
    stmt = (
        select(
            Entry_Db.id.label('entry_id'),
            Entry_Db.title.label('entry_title'),
            Source_Db.title.label('source_title'),
            Entry_Db.created_date,
        )
        .join(Source_Db, Entry_Db.source_id == Source_Db.id)
        .join(user_to_source, user_to_source.c.source_id == Source_Db.id)
        .where(user_to_source.c.user_id == user.id)
        .order_by(Entry_Db.created_date.desc())
        .limit(limit)
        .offset(offset)
    )
    return session.execute(stmt).all()


def get_entries_by_source(session, source_id: int, limit: int, offset: int = 0):
    stmt = (
        select(Entry_Db)
        .where(Entry_Db.source_id == source_id)
        .order_by(Entry_Db.created_date.desc())
        .limit(limit)
        .offset(offset)
    )
    return session.execute(stmt).scalars().all()


def count_source_entries(session, source_id: int) -> int:
    from sqlalchemy import func

    stmt = select(func.count(Entry_Db.id)).where(Entry_Db.source_id == source_id)
    return session.execute(stmt).scalar() or 0


def count_user_entries(session, user: User) -> int:
    from sqlalchemy import func

    stmt = (
        select(func.count(Entry_Db.id))
        .join(Source_Db, Entry_Db.source_id == Source_Db.id)
        .join(user_to_source, user_to_source.c.source_id == Source_Db.id)
        .where(user_to_source.c.user_id == user.id)
    )
    return session.execute(stmt).scalar() or 0
