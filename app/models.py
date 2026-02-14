from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


user_to_source = Table(
    'user_to_source',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('source_id', Integer, ForeignKey('sources.id'), primary_key=True),
)


class User(Base):
    __tablename__ = 'users'

    # todo: make id not consequential
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[bytes]

    sources = relationship('Source', secondary=user_to_source, back_populates='users')

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, name={self.name!r}, email={self.email!r})'


class Source(Base):
    __tablename__ = 'sources'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    link: Mapped[str]
    feed_link: Mapped[str] = mapped_column(unique=True)

    # todo: process correctly at `parse` level
    last_etag: Mapped[str | None]
    last_modified: Mapped[datetime | None]

    users = relationship('User', secondary=user_to_source, back_populates='sources')
    entries = relationship('Entry', back_populates='source')

    def __repr__(self) -> str:
        return f'Source(id={self.id!r}, title={self.title!r}, author={self.author!r})'


class Entry(Base):
    __tablename__ = 'entries'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    link: Mapped[str]
    summary: Mapped[str]
    content: Mapped[str]
    created_date: Mapped[datetime]
    # guid: Mapped[str]  # feed ID given by the source (to avoid duplicates)

    source_id: Mapped[int] = mapped_column(ForeignKey('sources.id'))
    source: Mapped['Source'] = relationship(back_populates='entries')

    def __repr__(self) -> str:
        return f'Entry(id={self.id!r}, title={self.title!r})'
