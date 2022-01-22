import sys
from typing import List, Optional

from ninja import Router, File
from django.contrib.auth import get_user_model
from pydantic.types import UUID4

from account.authorization import GlobalAuth
from config.utils.schemas import MessageOut
from news.models import Article, Category, Image, ArticleImage
from news.schemas import ArticleOut, ArticleIn
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ninja.files import UploadedFile
from django.utils.encoding import uri_to_iri
import json

article_controller = Router(tags=["Articles"])

User = get_user_model()


@article_controller.get("articles", response={200: List[ArticleOut], 404: MessageOut})
def get_articles(request, filter: Optional[str] = None, category: Optional[str] = None):
    articles_qs = Article.objects.all()

    # if filter parameter is provided
    if filter:
        try:
            filter_params = json.loads(filter)
            # search
            if "q" in filter_params:
                q = filter_params["q"]
                articles_qs = articles_qs.filter(
                    Q(title__icontains=q) | Q(content__icontains=q)
                )
            # language
            if "lang" in filter_params:
                lang = filter_params["lang"]
                if lang in ["en", "ar"]:
                    articles_qs = articles_qs.filter(language=lang)

        except KeyError:
            pass
        except json.decoder.JSONDecodeError:
            pass

    # filters category
    if category and category in list(Category.objects.values_list('slug', flat=True)):
        articles_qs = articles_qs.filter(category=Category.objects.get(slug=category).id)

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
@article_controller.post("articles", auth=GlobalAuth(), response={
    201: ArticleOut,
    401: MessageOut
})
def post_article(request, article_in: ArticleIn, images: List[UploadedFile] = File(...)):
    # checks if the token is valid or exists
    if 'pk' not in request.auth:
        return 401, {'detail': 'unauthorized'}
    # gets the user from pk
    user = User.objects.filter(id=request.auth['pk'])[0]
    if user.is_staff:
        article = Article(**article_in.dict(), author_id=user.id)
        article.save()
        for image in images:
            image = Image(image_url=image)
            image.save()
            article_image = ArticleImage(article_id=article, image_id=image)
            article_image.save()
        return 201, article
    return 401, {'detail': 'unauthorized'}


# TODO Update post endpoint + authentication
@article_controller.put("/articles/{id}", response={
    200: MessageOut
})
def update_article(request, id: UUID4, article_in: ArticleIn):
    article = get_object_or_404(Article, id=id)
    for attr, value in article_in.dict().items():
        setattr(article, attr, value)
    article.save()
    return {"detail": "success"}


# TODO Delete Post endpoint + authentication
@article_controller.delete("/articles/{id}", response={
    204: MessageOut,
})
def delete_article(request, id: UUID4):
    article = get_object_or_404(Article, id=id)
    article.delete()
    return 204, {"detail": ""}
