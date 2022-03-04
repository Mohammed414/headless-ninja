from django.db import models
from django.contrib.auth import get_user_model

from config.utils.models import Entity

User = get_user_model()


class Category(Entity):
    parent = models.ForeignKey('self',
                               verbose_name='parent',
                               related_name='children',
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=75)
    slug = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


# class that connects user and category
class UserCategory(models.Model):
    user = models.ForeignKey(User,
                             verbose_name='user',
                             related_name='categories',
                             on_delete=models.CASCADE)
    category = models.ForeignKey('Category',
                                 verbose_name='category',
                                 related_name='users',
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'User Category'
        verbose_name_plural = 'User Categories'

    def __str__(self):
        return f'{self.user} - {self.category}'
