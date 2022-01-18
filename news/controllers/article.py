from typing import List, Optional

from ninja import Router, File
from django.contrib.auth import get_user_model
from pydantic.types import UUID4
from config.utils.schemas import MessageOut
from news.models import Article, Category, Image, ArticleImage
from news.schemas import ArticleOut, ArticleIn
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ninja.files import UploadedFile

article_controller = Router(tags=["Articles"])

User = get_user_model()


@article_controller.get("articles", response={200: List[ArticleOut], 404: MessageOut})
def get_articles(request, language: Optional[str] = None, category: Optional[str] = None, q: Optional[str] = None):
    articles_qs = Article.objects.all()
    # filters language
    if language and language in ["ar", "en"]:
        articles_qs = articles_qs.filter(language=language)

    # filters category
    if category and category in list(Category.objects.values_list('slug', flat=True)):
        articles_qs = articles_qs.filter(category=Category.objects.get(slug=category).id)

    # handles search
    if q:
        articles_qs = articles_qs.filter(
            Q(title__icontains=q) | Q(content__icontains=q)
        )
    return articles_qs


# get an article with an id
@article_controller.get("/articles/{article_id}", response={
    200: ArticleOut,
    404: MessageOut
})
def retrieve_article(request, article_id: UUID4):
    return get_object_or_404(Article, id=article_id)


# TODO authentication
# post an article with one or multiple images
@article_controller.post("articles", response={
    200: ArticleOut
})
def post_article(request, article_in: ArticleIn, images: List[UploadedFile] = File(...)):
    article = Article(**article_in.dict())
    article.save()
    for image in images:
        image = Image(image_url=image)
        image.save()
        article_image = ArticleImage(article_id=article, image_id=image)
        article_image.save()
    return article

# TODO Update post endpoint + authentication


# TODO Delete Post endpoint + authentication

# TODO GET ALL CATEGORIES

# TODO Create Category

# TODO update a category

# TODO delete a category
