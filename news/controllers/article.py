from typing import List

from ninja import Router
from django.contrib.auth import get_user_model

from config.utils.schemas import MessageOut
from news.models import Article, Category
from news.schemas import ArticleOut

article_controller = Router(tags=["Articles"])

User = get_user_model()


@article_controller.get("{language}/{category}/articles", response={200: List[ArticleOut], 404: MessageOut})
def get_posts(request, language: str, category):
    # checks if the language exists
    if language not in ["ar", "en"]:
        return 404, {"detail": "Page not found"}
    # checks if the category exists
    if category not in list(Category.objects.values_list('slug', flat=True)):
        return 404, {"detail": "Page not found"}
    # gets the category id (section id)
    category_id = Category.objects.get(slug=category).id

    return Article.objects.all().filter(language=language, category=category_id)
