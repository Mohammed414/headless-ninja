from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, UserAdmin
from guardian.admin import GuardedModelAdmin

from account.forms import UserAdminChangeForm, UserAdminCreationForm
from account.models import User

#
# class UserAdmin(BaseUserAdmin):
#     # The forms to add and change user instances
#     form = UserAdminChangeForm
#     add_form = UserAdminCreationForm
#
#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
#     list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser',)
#     list_filter = ('is_superuser', 'is_staff')
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': (
#             'first_name', 'last_name', 'phone_number')}),
#         ('Permissions',
#          {'fields': ( 'is_active', 'is_superuser', 'is_staff', 'is_verified', 'groups', 'user_permissions',)}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2')}
#          ),
#     )
#     search_fields = ('first_name', 'last_name', 'email')
#     ordering = ('email',)
#     filter_horizontal = ()
from news.models.category_models import UserCategory


class UserCategoryInline(admin.TabularInline):
    model = UserCategory
    extra = 1


class AuthorAdmin(UserAdmin):
    # don't show inlines only for superuser
    def get_inline_instances(self, request, obj=None):
        if obj:
            if obj.is_superuser:
                self.inlines = []
            else:
                self.inlines = [UserCategoryInline]
        return super(AuthorAdmin, self).get_inline_instances(request, obj)

    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser',)
    list_filter = ('is_superuser', 'is_staff')
    fieldsets = (
        ("Account", {'fields': ('email', 'password')}),

        ('Personal info', {'fields': (
            'first_name', 'last_name', 'phone_number')}),

        ('Permissions',
         {'fields': ('is_active', 'is_superuser', 'is_staff', 'is_verified', 'groups', 'user_permissions',)}),

        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, AuthorAdmin)
