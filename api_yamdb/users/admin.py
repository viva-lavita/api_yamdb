from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'email',
                    'confirmation_code',
                    'first_name',
                    'last_name',
                    'bio',
                    'role',)
    search_fields = ('username',)
    list_filter = ('role',)
    list_editable = ('role',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
