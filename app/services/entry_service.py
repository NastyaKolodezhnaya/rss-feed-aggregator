from dataclasses import asdict

from sqlalchemy.sql.expression import select

from app.models import Entry as Entry_Db
from app.models import Source as Source_Db
from app.models import user_to_source
from app.utils.parse import ParsedEntry


def add_new_entries(session, entries: list[ParsedEntry]):
    final_entries = []
    for entry in entries:
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


def get_all_user_entries(session, user_id: int, n: int):
    stmt = (
        select(Entry_Db.title, Source_Db.title, Entry_Db.created_date)
        .join(Source_Db, Entry_Db.source_id == Source_Db.id)
        .join(user_to_source, user_to_source.c.source_id == Source_Db.id)
        .where(user_to_source.c.user_id == user_id)
        .order_by(Entry_Db.created_date.desc())
        .limit(n)
    )
    return session.execute(stmt).all()
