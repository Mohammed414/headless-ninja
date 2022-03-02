from django.contrib import admin
from django.forms import Textarea
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db import models

from news.models import Article, Category, ArticleImage, Image

# admin.site.register(Article)
admin.site.register(Category)
admin.site.register(ArticleImage)


# admin.site.register(Image)


class ArticleImageInline(admin.StackedInline):
    model = ArticleImage
    extra = 1
    field = ('image', 'render_image')
    readonly_fields = ('render_image',)

    def render_image(self, obj):
        # if the object doesn't have image return empty string
        return mark_safe('<a href={url}><img src="{url}" width="{width}" height={height} /></a>'.format(
            url=obj.image_id.image_url.url,
            width=300,
            height=300,
        )
        )


# class ArticleImageInline(admin.StackedInline):
#     # show article image in article admin page
#     def image_tag(self, obj):
#         print("2")
#         return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" />')
#     readonly_fields = ('image_tag',)
#     model = ArticleImage
#     extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = 'author', 'language', 'status', 'title', 'category', "published_at"
    list_filter = ('category',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'title': ('title',)}
    ordering = ('-published_at',)
    inlines = [ArticleImageInline]

    """
    For non-superuser users, only show articles that are theirs 
    """

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    """
    here, if the user is superuser then he can publish, edit, delete on the behalf of all the users
    But, if the user is not superuser then he can only publish, edit, delete on his behalf
    """

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.author = request.user
        obj.save()


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     pass
#     list_display = ('name', 'created_at', 'updated_at')
#     search_fields = ('name',)
#     prepopulated_fields = {'slug': ('name',)}
#     ordering = ('-created_at',)


# @admin.register(ArticleImage)
# class ArticleImageAdmin(admin.ModelAdmin):
#     # list_display = ('article', 'image', 'created_at', 'updated_at')
#     # list_filter = ('article',)
#     # search_fields = ('article', 'image')
#     # ordering = ('-created_at',)
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    readonly_fields = ["preview"]

    def preview(self, obj):
        return mark_safe('<a href={url}><img src="{url}" width="{width}" height={height} /></a>'.format(
            url=obj.image_url.url,
            width="300",
            height="300",
        )
        )
