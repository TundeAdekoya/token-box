from django.contrib import admin
from .models import User

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'first_name', 'last_name', 'staff', 'admin', 'active']
    list_editable = ['staff', 'admin', 'active']

admin.site.register(User,CustomUserAdmin)
