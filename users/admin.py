from django.contrib import admin

from users.models import UserModel


# Register your models here.
@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name')
    list_filter = ('is_staff', 'last_name', 'date_joined')
    filter_horizontal = ('groups',)
    fields = ('username', 'first_name', 'last_name', 'is_verified', 'image', 'email', 'password', 'groups',)
