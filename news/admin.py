from django.contrib import admin

from news.models import Post, PostCategory, PostTag, Category, Tag

admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(PostTag)
admin.site.register(Category)
admin.site.register(Tag)
