from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

# todo:  add proper request structures


class ConfiguredModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class User(ConfiguredModel):
    id: int
    username: str
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


class SourceSummary(ConfiguredModel):
    id: int
    title: str
    author: str
    link: str
    feed_link: str


class Source(SourceSummary):
    last_etag: str | None = None
    last_modified: datetime | None = None
    entries: list[Entry] = []


class EntryBrief(ConfiguredModel):
    entry_title: str
    source_title: str
    created_date: datetime


# --- Response wrappers ---


class SourceListResponse(BaseModel):
    sources: list[SourceSummary]


class SourceResponse(BaseModel):
    source: Source


class EntryListResponse(BaseModel):
    entries: list[Entry]


class EntryResponse(BaseModel):
    entry: Entry


class EntryBriefListResponse(BaseModel):
    entries: list[EntryBrief]


class AuthFormRequest(BaseModel):
    username: str
    password: str
