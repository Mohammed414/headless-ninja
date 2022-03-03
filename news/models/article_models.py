import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe

from config.utils.models import Entity
from news.models import Category
from django.utils.text import slugify

User = get_user_model()


class Article(Entity):
    class ArticleObjects(models.Manager):
        def get_queryset(self):
            return super().get_query_set().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    language_options = (
        ("ar", "ar"),
        ("en", "en")
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    language = models.CharField(max_length=7, choices=language_options, default='ar')

    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    slug = models.SlugField(max_length=250, editable=False)
    status = models.CharField(max_length=10, choices=options, default='published')
    published_at = models.DateTimeField(blank=True, null=True)

    content = models.TextField()

    images = models.ManyToManyField('Image', blank=True)

    objects = models.Manager()
    article_objects = ArticleObjects()  # this is a custom manager

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ('-published_at',)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Article, self).save(*args, **kwargs)


class Image(Entity):
    image_url = models.ImageField('image', upload_to='images')

    # change the image name to uuid4 because we can't have duplicate image names
    def save(self, *args, **kwargs):
        if self.image_url.name:
            self.image_url.name = f"{uuid.uuid4().hex}.{self.image_url.name.split('.')[1]}"

        super(Image, self).save(*args, **kwargs)

    # on delete delete the image from the folder
    def delete(self, *args, **kwargs):
        self.image_url.delete()
        super(Image, self).delete(*args, **kwargs)

    def __str__(self):
        return self.image_url.name


class ArticleImage(Entity):
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    image_id = models.ForeignKey(Image, on_delete=models.CASCADE)

    # on delete delete the image from the folder
    def delete(self, *args, **kwargs):
        self.image_id.delete()
        super(ArticleImage, self).delete(*args, **kwargs)

    def __str__(self):
        return self.article_id.title
