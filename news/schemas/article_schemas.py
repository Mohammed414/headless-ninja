from datetime import datetime, time
from typing import Optional, List

from ninja import Schema, UploadedFile, File
from ninja.orm import create_schema
from pydantic.types import UUID4, FilePath

from news.models import Article


class UUIDSchema(Schema):
    id: UUID4


class ArticleOut(UUIDSchema):
    published_at: datetime
    title: str
    content: str


class ArticleIn(Schema):
    title: str
    language: str
    category_id: UUID4
    meta_title: str
    meta_description: str
    status: str
    published_at: datetime
    content: str


class ArticleSchema(ArticleIn):
    id: UUID4
