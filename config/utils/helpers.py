from pydantic import UUID4

from news.models import ArticleImage


# a function that return article images
def get_article_images(article_id: UUID4):
    post_images = ArticleImage.objects.filter(article_id=article_id)
    if not post_images:
        return []
    images_urls = []
    for link in post_images:
        # get images urls
        images_urls.append("media/" + link.image_id.__str__())
    return images_urls
