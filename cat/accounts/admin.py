from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Accounts
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(Accounts)
class AccountsAdmin(ModelAdmin):
    list_display = ("name", "surname", "email", "created_at", "updated_at")
    search_fields = ("name", "surname", "email")
    list_filter = ("created_at", "updated_at")
    ordering = ("-created_at",)
    readonly_fields = ("password", "created_at", "updated_at")
    fields = ("name", "surname", "email", "password", "created_at", "updated_at")


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
