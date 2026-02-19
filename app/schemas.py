from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

# todo:  add proper request structures


class ConfiguredModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class User(ConfiguredModel):
    id: int
    name: str
    email: str  # todo: add email validation
    password: str = Field(min_length=8)


class Entry(ConfiguredModel):
    id: int
    title: str
    link: str
    summary: str
    content: str
    created_date: datetime
    source_id: int
    # guid: int  # feed ID given by the source (to avoid duplicates)


class Source(ConfiguredModel):
    title: str
    author: str
    link: str
    feed_link: str
    last_etag: str
    last_modified: datetime

    entries: list[Entry]


# class AddSourceRequest(BaseModel):
#     feed_link: str
#     user_id: int  # later this comes from auth, not the request


class AuthFormRequest(BaseModel):
    username: str
    password: str
