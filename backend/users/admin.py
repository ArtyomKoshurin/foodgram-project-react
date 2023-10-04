from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name',
                    'last_name', 'password',)
    search_fields = ('username',)
    list_filter = ('username', 'email',)
    list_editable = ('password',)
    empty_value_display = '-пусто-'


admin.site.register(CustomUser, CustomUserAdmin)
