import uuid
from collections import OrderedDict
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, Union


@dataclass(frozen=True)
class Base:
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class Filmwork(Base):
    title: str
    description: Optional[str]
    creation_date: Optional[date]
    rating: Union[float, int, None]
    type: str
    file_path: Optional[str]


@dataclass(frozen=True)
class Genre(Base):
    name: str
    description: Optional[str]


@dataclass(frozen=True)
class GenreFilmwork:
    id: uuid.UUID
    genre_id: uuid.UUID
    film_work_id: uuid.UUID
    created_at: Optional[datetime]


@dataclass(frozen=True)
class Person(Base):
    full_name: str


@dataclass(frozen=True)
class PersonFilmwork:
    id: uuid.UUID
    person_id: uuid.UUID
    film_work_id: uuid.UUID
    role: str
    created_at: datetime


tables = OrderedDict([
    ('film_work', Filmwork),
    ('genre', Genre),
    ('genre_film_work', GenreFilmwork),
    ('person', Person),
    ('person_film_work', PersonFilmwork)
])
