from dataclasses import asdict

from sqlalchemy import select

from app.models import Entry as Entry_Db
from app.models import Source as Source_Db
from app.utils.parse import construct_new_feed


def source_exists(session, feed_link: str):
    stmt = select(Source_Db).where(Source_Db.feed_link == feed_link)
    result = session.execute(stmt)
    return result.scalars().first() or None


def create_source(session, feed_link: str):
    source_data = construct_new_feed(feed_link)

    source_kwargs = asdict(source_data)
    entries_kwargs = source_kwargs.pop('entries')

    source_db = Source_Db(**source_kwargs, entries=[Entry_Db(**e) for e in entries_kwargs])

    session.add(source_db)
    session.commit()
