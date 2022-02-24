import uuid
from typing import List, Optional

from django.core.paginator import Paginator, EmptyPage
from ninja import Router, File
from django.contrib.auth import get_user_model
from pydantic.types import UUID4

from account.authorization import GlobalAuth
from config.utils.helpers import get_article_images
from config.utils.schemas import MessageOut
from news.models import Article, Category, Image, ArticleImage
from news.schemas import ArticleOut, ArticleIn, ImagesOut
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ninja.files import UploadedFile
import json

article_controller = Router(tags=["Articles"])

User = get_user_model()


@article_controller.get("", response={200: List[ArticleOut], 404: MessageOut})
def get_articles(request, range: Optional[str] = None, page: Optional[int] = 1, filter: Optional[str] = None):
    articles_qs = Article.objects.all().filter(language='en')
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
            # category filter
            if "cat" in filter_params:
                cat = filter_params["cat"]
                if cat in list(Category.objects.values_list('slug', flat=True)):
                    articles_qs = articles_qs.filter(category=Category.objects.get(slug=cat).id)

            # order filter
            if "order" in filter_params:
                order = filter_params["order"]
                if order in ["asc", "desc"]:
                    articles_qs = articles_qs.order_by("-created_at" if order == "desc" else "created_at")

        except KeyError:
            pass
        except json.decoder.JSONDecodeError:
            pass
    """Range pagination starts here """
    # TODO catch range error

    if range:
        # get range list
        try:
            range = json.loads(range)
        except ValueError:
            return 404, {"message": "Error"}

        # articles per page
        per_page = range[1] + 1 - range[0]

        # now we paginate the articles
        paginator = Paginator(articles_qs, per_page)

        # get page number from range
        page_number = (range[1] + 1) / per_page

        try:
            page = paginator.page(page_number)
        except EmptyPage:
            return 404, {"message": "Page not found"}
        articles = page.object_list
        setattr(request, 'number_of_rows', len(articles_qs))
        # add images to articles
        for article in articles:
            article.images = get_article_images(article.id)
        # return paginated articles
        return articles
        """Range pagination ends here """

    """
    Page pagination (another option)
    """
    if page:
        # add image for each article
        articles = []
        for article in articles_qs:
            article_images = get_article_images(article.id)
            article.images = article_images
            articles.append(article)
        # paginate the articles
        paginator = Paginator(articles_qs, 10)
        try:
            page = paginator.page(page)
            return page.object_list
        except EmptyPage:
            return 404, {"message": "Page not found"}

    """Page pagination ends here"""

    return articles_qs


# get an article with an id
@article_controller.get("{article_id}", response={
    200: ArticleOut,
    404: MessageOut
})
def retrieve_article(request, article_id: UUID4):
    article = get_object_or_404(Article, id=article_id)
    article.__dict__['images'] = get_article_images(article_id)
    return article


# TODO AUTH
# post an article with one or multiple images
@article_controller.post("", auth=GlobalAuth(), response={
    201: ArticleOut,
    401: MessageOut
})
def post_article(request, article_in: ArticleIn, images: List[UploadedFile] = File(...)):
    # checks if the token is valid or exists
    if 'pk' not in request.auth:
        return 401, {'message': 'unauthorized'}
    # gets the user from pk
    user = User.objects.filter(id=request.auth['pk'])[0]
    # print user email
    print(user.email)

    if user.is_staff:
        article = Article(**article_in.dict(), author_id=user.id)
        article.save()
        for image in images:
            # make a random image name using uuid4 + image extension
            image.name = f"{uuid.uuid4().hex}.{image.name.split('.')[1]}"
            image = Image(image_url=image)
            image.save()
            article_image = ArticleImage(article_id=article, image_id=image)
            article_image.save()
        return 201, article
    return 401, {'message': 'unauthorized'}


# TODO AUTH
@article_controller.put("{article_id}", response={
    200: ArticleOut
})
def update_article(request, article_id: UUID4, article_in: ArticleIn):
    article = get_object_or_404(Article, id=article_id)
    for attr, value in article_in.dict().items():
        setattr(article, attr, value)
    article.save()
    return article


# TODO AUTH
@article_controller.delete("{article_id}", response={
    204: MessageOut,
})
def delete_article(request, article_id: UUID4):
    article = get_object_or_404(Article, id=article_id)
    article.delete()
    return 204, {"message": ""}
