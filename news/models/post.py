from django.db import models
from django.contrib.auth import get_user_model
from config.utils.models import Entity
from news.models import Category

User = get_user_model()


class Post(Entity):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=75)
    title_en = models.CharField(max_length=75, default="Title")
    metatitle = models.CharField(db_column='metaTitle', max_length=100, blank=True, null=True)
    slug = models.CharField(unique=True, max_length=100)
    summary = models.TextField(blank=True, null=True)
    summary_en = models.TextField(blank=True, null=True)
    published = models.IntegerField()
    published_at = models.DateTimeField(blank=True, null=True)
    content_ar = models.TextField(blank=True, null=True)
    content_en = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'


class PostCategory(Entity):
    post_id = models.OneToOneField(Post, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Post Category"
        verbose_name_plural = "Post Categories"


class PostTag(Entity):
    post_id = models.OneToOneField(Post, on_delete=models.CASCADE)
    tag_id = models.ForeignKey('Tag', on_delete=models.CASCADE)
