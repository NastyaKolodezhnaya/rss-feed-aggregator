from dataclasses import dataclass
from datetime import datetime

import feedparser


@dataclass
class ParsedEntry:
    title: str
    link: str
    summary: str
    content: str
    created_date: datetime


@dataclass
class ParsedSource:
    title: str
    author: str
    link: str
    feed_link: str
    last_etag: str
    last_modified: datetime
    entries: list[ParsedEntry]


def parse_feed_datetime(date_str: str):
    return datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')


def parse_entry_datetime(date_str: str):
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')


def construct_new_feed(feed_link: str):
    source = feedparser.parse(feed_link)
    entries = [construct_entry(e) for e in source.entries]

    return ParsedSource(
        title=source.feed.title,
        author=source.feed.author,
        link=source.feed.link,
        feed_link=source.feed.id,
        last_etag=source.etag,
        last_modified=parse_feed_datetime(source.updated),
        entries=entries,
    )


def construct_entry(entry):
    content = '<p>'.join(c.value for c in entry.content)  # todo: see how it's going with multiple content
    return ParsedEntry(
        title=entry.title,
        link=entry.link,
        summary=entry.summary,
        content=content,
        created_date=parse_entry_datetime(entry.updated),
    )


def parse_feed(feed_link: str, last_etag: str, last_modified: datetime):
    res = feedparser.parse(feed_link, etag=last_etag, modified=last_modified)
    if res.status == '304':
        return None
    return [construct_entry(e) for e in res.entries]
