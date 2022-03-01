from django.contrib import admin

from news.models import Article, Category, ArticleImage, Image

# admin.site.register(Article)
admin.site.register(Category)
admin.site.register(ArticleImage)
admin.site.register(Image)


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1


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

    # change field depending on the user type
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        return ['author']

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
# @admin.register(Image)
# class ImageAdmin(admin.ModelAdmin):
#     list_display = ('name', 'created_at', 'updated_at')
#     search_fields = ('name',)
#     ordering = ('-created_at',)
