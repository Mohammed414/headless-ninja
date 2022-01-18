from django.contrib import admin

from news.models import Article, Category, ArticleImage, Image

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(ArticleImage)
admin.site.register(Image)

