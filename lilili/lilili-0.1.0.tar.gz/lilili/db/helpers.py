from typing import List, Optional

from sqlalchemy.orm.session import Session

from .defs import Domain, Library


def query_library(
    session: Session, domain: Domain, name: str, version: str
) -> Optional[Library]:
    return (
        session.query(Library)
        .filter(
            Library.domain == domain,
            Library.name == name,
            Library.version == version,
        )
        .one_or_none()
    )


def query_library_by_name(session: Session, name: str) -> List:
    libraries = session.query(Library).filter(Library.name.like(f"%{name}%")).all()
    return [library.to_dict() for library in libraries]


def add_library(session: Session, library: Library) -> None:
    session.add(library)
    session.commit()
