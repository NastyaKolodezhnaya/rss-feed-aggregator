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


# todo: process attributes absence more robust
def get_attr_safe(obj, attr):
    try:
        return getattr(obj, attr)
    except AttributeError:
        return 'unknown'


def construct_new_feed(feed_link: str):
    source = feedparser.parse(feed_link)
    if not (source.feed and source.entries):
        if source.bozo:  # some failures during the fetching
            return source.bozo_exception
        return None

    entries = [construct_entry(e) for e in source.entries]

    return ParsedSource(
        title=source.feed.title,
        author=get_attr_safe(source.feed, 'author'),
        link=source.feed.link,
        feed_link=source.feed.id,
        last_etag=source.etag,
        last_modified=parse_feed_datetime(source.updated),
        entries=entries,
    )


def construct_entry(entry):
    if content := entry.get('content', None):
        content = '<p>'.join(c.value for c in content)
    else:
        content = entry.get('summary', '')

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


if __name__ == '__main__':
    link = 'https://samwho.dev/rss.xml'
    res = construct_new_feed(link)
    print(res)
