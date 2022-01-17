from datetime import datetime, time

from ninja import Schema
from pydantic.types import UUID4


class UUIDSchema(Schema):
    id: UUID4


class ArticleOut(UUIDSchema):
    published_at: datetime
    title: str
    content: str
