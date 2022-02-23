from datetime import datetime
from typing import Optional, List
from ninja.files import UploadedFile
from ninja import File

from ninja import Schema
from pydantic.networks import EmailStr
from pydantic.types import UUID4
from django.contrib.auth import get_user_model
from ninja import ModelSchema

from news.models import Article


class UUIDSchema(Schema):
    id: UUID4


class Category(Schema):
    title: str
    slug: str
    description: str


class CategoryOut(Schema):
    title: str
    slug: str


class AccountOut(Schema):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str]


class ArticleOut(ModelSchema):
    category: CategoryOut
    images: Optional[List[str]] = []

    class Config:
        model = Article
        model_fields = ["id", "title", "language", "category", "published_at",
                        "content"]


class ArticleIn(Schema):
    title: str
    language: str
    category_id: UUID4
    status: str
    published_at: datetime
    content: str


class ArticleSchema(ArticleIn):
    id: UUID4


class ImagesOut(Schema):
    images: List[str]
