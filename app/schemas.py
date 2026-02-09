from datetime import datetime

from pydantic import BaseModel, Field

# todo:  add proper request structures


class User(BaseModel):
    name: str
    email: str  # todo: add email validation
    password: str = Field(min_length=8)


class Entry(BaseModel):
    id: int
    title: str
    link: str
    summary: str
    content: str
    created_date: datetime
    source_id: int
    # guid: int  # feed ID given by the source (to avoid duplicates)


class AddSourceRequest(BaseModel):
    feed_link: str
    user_id: int  # later this comes from auth, not the request


class Source(BaseModel):
    title: str
    author: str
    link: str
    feed_link: str
    last_etag: str
    last_modified: datetime

    entries: list[Entry]
