# a function that return article images
from pydantic import UUID4

from news.models import ArticleImage


def get_article_images(article_id: UUID4):
    post_images = ArticleImage.objects.filter(article_id=article_id)
    if not post_images:
        return []
    images_urls = []
    for link in post_images:
        # get the right image url for each image
        """
        could be better. for now it's just a duct tape solution
        """
        images_urls.append(link.image_id.__str__()[4:])
    return images_urls