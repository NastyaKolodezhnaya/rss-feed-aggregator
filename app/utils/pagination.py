import math
from dataclasses import dataclass

PER_PAGE = 20


@dataclass
class Pagination:
    page: int
    total_pages: int
    offset: int
    limit: int


def paginate(total: int, page: int, per_page: int = PER_PAGE) -> Pagination:
    total_pages = max(1, math.ceil(total / per_page))
    page = min(page, total_pages)
    offset = (page - 1) * per_page
    return Pagination(page=page, total_pages=total_pages, offset=offset, limit=per_page)
