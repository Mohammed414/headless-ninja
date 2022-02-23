import time
from typing import List

from ninja import Router
from pydantic.types import UUID4

from config.utils.schemas import MessageOut
from news.models import Category, Article
from news.schemas import CategorySchema, CategoryIn
from django.shortcuts import get_object_or_404

category_controller = Router(tags=["Category"])


# TODO GET ALL CATEGORIES
@category_controller.get("/categories", response={
    200: List[CategorySchema]
})
def get_categories(request):
    return Category.objects.all()


# TODO AUTH
@category_controller.get("/categories/{category_id}", response={
    200: CategorySchema,
    404: MessageOut
})
def get_category(request, category_id: UUID4):
    category = get_object_or_404(Category, id=category_id)
    return category


# TODO AUTH
@category_controller.post("/categories", response={
    201: CategorySchema
})
def create_category(request, category_in: CategoryIn):
    category = Category(**category_in.dict())
    category.save()
    return category


# TODO AUTH
@category_controller.put("/categories/{category_id}", response={
    200: CategorySchema,
    404: MessageOut
})
def update_category(request, category_id: UUID4, category_in: CategoryIn):
    category = get_object_or_404(Category, id=category_id)
    for attr, value in category_in.dict().items():
        setattr(category, attr, value)
    category.save()
    return category


# TODO AUTH
@category_controller.delete("/categories/{category_id}", response={204: MessageOut,
                                                                   404: MessageOut
                                                                   })
def delete_category(request, category_id: UUID4):
    category = get_object_or_404(Category, id=category_id)
    # we first need to make all the posts of category x to the default category -uni
    posts_with_category = Article.objects.filter(category_id=category.id)
    default_category_id = get_object_or_404(Category, slug="uni")
    for post in posts_with_category:
        post.category = default_category_id
        post.save()

    category.delete()
    return 204, {"message": ""}
