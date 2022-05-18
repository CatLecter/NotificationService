from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class PrimaryData(BaseModel):
    id: UUID
    created_at: datetime
    last_update: datetime
    notification_id: UUID
    last_notification_send: Optional[datetime] = None
    source: str
    event_type: str
    content_uuid: UUID
    action: str
    data_endpoint: str
    in_queue: bool
    recipient_uuid: UUID


class GenreBrief(BaseModel):
    """Жанр фильма."""

    uuid: str
    name: str


class PersonBrief(BaseModel):
    """Персона фильма."""

    uuid: str
    full_name: str


class Role(BaseModel):
    """Роль пользователя."""

    uuid: UUID
    name: str


class User(BaseModel):
    """Модель пользователя."""

    uuid: UUID
    created_at: datetime
    username: str
    email: str
    is_active: bool
    is_superuser: bool
    roles: list[Role]
    is_totp_enabled: bool


class Film(BaseModel):
    """Модель фильма."""

    uuid: str
    title: str
    imdb_rating: Optional[float]
    description: Optional[str]
    genres: list[GenreBrief]
    directors: list[PersonBrief]
    writers: list[PersonBrief]
    actors: list[PersonBrief]


class ResponseModel(BaseModel):
    email: str
    templates_type: Enum
    data: dict
