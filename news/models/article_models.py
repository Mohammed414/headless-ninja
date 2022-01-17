from django.db import models
from django.contrib.auth import get_user_model
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

    title = models.CharField(max_length=75)
    language = models.CharField(max_length=7, choices=language_options, default='ar')

    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    slug = models.SlugField(max_length=250, editable=False)
    meta_title = models.CharField(max_length=100, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=10, choices=options, default='published')
    published_at = models.DateTimeField(blank=True, null=True)

    content = models.TextField()

    image = models.ImageField('image', upload_to='articles_images/')

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
