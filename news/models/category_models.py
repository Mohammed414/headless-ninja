from django.db import models

from config.utils.models import Entity


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
