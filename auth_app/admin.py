from django.contrib import admin
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    search_fields = ('email',)
    list_display = ('email', 'first_name', 'last_name')

admin.site.register(User, UserAdmin)