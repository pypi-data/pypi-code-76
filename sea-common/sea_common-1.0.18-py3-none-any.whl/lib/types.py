from typing import Generic, List, Optional, Tuple, TypeVar
from enum import Enum
from datetime import datetime
from base64 import b64encode, b64decode
import strawberry
from flask_sqlalchemy import Pagination

T = TypeVar('T')


@strawberry.interface
class Node:
    id: strawberry.ID


@strawberry.type(description='A list of edges.')
class Edge(Generic[T]):
    node: T
    cursor: str


@strawberry.type(description='Information to assist with pagination.')
class PageInfo:
    start_cursor: Optional[str]
    end_cursor: Optional[str]
    has_next_page: bool
    has_previous_page: bool


@strawberry.type(description='A list of edges with pagination information.')
class Connection(Generic[T]):
    edges: List[Edge[T]]
    page_info: PageInfo
    total_count: int
    filtered_count: int
    page_count: int
    current_page: int

    @classmethod
    def load(cls, data: Pagination, counts: Tuple[int, int]):
        return Connection(
            [Edge(item, to_cursor_hash(item.created_at)) for item in data.items],
            PageInfo(
                to_cursor_hash(data.items[0].created_at) if data.items else None,
                to_cursor_hash(data.items[-1].created_at) if data.items else None,
                data.has_next,
                data.has_prev,
            ),
            *counts,  # total_count and filtered_count
            data.pages,  # page_count
            data.page,  # current_page
        )


def to_cursor_hash(created_at: datetime) -> str:
    return str(b64encode(str(created_at).encode('utf-8')), 'utf-8')


def from_cursor_hash(cursor: str) -> datetime:
    return datetime.fromisoformat(str(b64decode(cursor), 'utf-8'))


@strawberry.enum(description='Selection of organisms.')
class OrganismSelect(Enum):
    NONE = ''
    HUMAN = 'human'
    MOUSE = 'mouse'
    RAT = 'rat'


organism_mapping = {
    'human': 9606,
    'mouse': 10090,
    'rat': 10116,
}


@strawberry.input
class InputWithOrganism:
    organism: Optional[OrganismSelect] = ''


@strawberry.interface
class MutationResponse:
    success: bool
    message: str
