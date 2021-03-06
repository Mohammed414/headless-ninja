from news.schemas import UUIDSchema
from ninja import Schema


class CategoryIn(Schema):
    title: str
    description: str
    slug: str


class CategorySchema(CategoryIn, UUIDSchema):
    pass
