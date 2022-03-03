import uuid

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.forms import Textarea
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db import models
from guardian.admin import GuardedModelAdmin

from news.models import Article, Category, ArticleImage, Image

admin.site.register(ArticleImage)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


class ArticleImageInline(admin.StackedInline):
    model = ArticleImage
    extra = 1
    field = ('image', 'render_image')
    readonly_fields = ('preview',)

    def preview(self, obj):
        # if the object doesn't have image return empty string
        return mark_safe('<a href={url}><img src="{url}" width="{width}" height={height} /></a>'.format(
            url=obj.image_id.image_url.url,
            width=300,
            height=300,
        )
        )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = 'author', 'language', 'status', 'title', 'category', "published_at"
    list_filter = ('category', 'status', 'language', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'title': ('title',)}
    ordering = ('-published_at',)
    inlines = [ArticleImageInline]
    exclude = ('images',)

    # TODO alter category field only show categories that are in user's permissions
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'category':
    #         kwargs['queryset'] = Category.objects.filter(
    #             pk__in=request.user.get_all_permissions().values_list('content_type_id', flat=True)
    #         )
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category' and request.user.is_superuser:
            kwargs['queryset'] = Category.objects.filter(title__startswith='c')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    """
    here, if the user is superuser then he can publish, edit, delete on the behalf of all the users
    But, if the user is not superuser then he can only publish, edit, delete on his behalf
    """

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    # remove author_id from the list of fields if the user is not superuser
    def get_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return 'title', 'content', 'category', 'status', 'language', 'published_at'
        return 'author', 'title', 'content', 'category', 'status', 'language', 'published_at'

    # if the post isn't their own, then they can't edit it (only superusers can)
    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if obj:
                return obj.author == request.user
            return False
        return True

    # nor delete it
    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if obj:
                return obj.author == request.user
            return False
        return True


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


admin.site.register(Permission)
