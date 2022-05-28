import email
from django.contrib import admin
from .models import UserAccount


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'email',
        'name',
        'is_active',
        'is_staff',
        # 'ís_admin',
        'is_superuser',
    ]


admin.site.register(UserAccount, UserAdmin)
