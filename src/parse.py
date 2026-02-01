import feedparser

link_rss = 'https://joshua.hu/feed.xml'
link_atom = 'https://www.martinfowler.com/feed.atom'

# rss = feedparser.parse(link_rss)


def parse_with_etag():
    atom = feedparser.parse(link_atom)
    etag = atom.etag

    atom1 = feedparser.parse(link_atom, etag=etag)
    etag1 = atom1.etag

    print(etag == etag1)
    print(atom1.status, getattr(atom1, 'debug_message', 'no message'))


def parse_with_modified():
    atom = feedparser.parse(link_atom)
    modified = atom.modified

    atom1 = feedparser.parse(link_atom, modified=modified)
    modified1 = atom1.modified

    print(modified == modified1)
    print(atom1.status, getattr(atom1, 'debug_message', 'no message'))


if __name__ == '__main__':
    parse_with_etag()
    parse_with_modified()

