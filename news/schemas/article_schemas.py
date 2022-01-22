from datetime import datetime
from typing import Optional

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


class AccountOut(Schema):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str]


class ArticleOut(ModelSchema):
    category: Category

    class Config:
        model = Article
        model_fields = ["id", "title", "language", "category", "meta_title", "meta_description", "published_at",
                        "content"]


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
