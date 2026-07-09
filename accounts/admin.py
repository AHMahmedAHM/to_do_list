from django.contrib import admin
from .models import CustomUser
# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone_number', 'is_active','is_staff', 'is_superuser']
    list_display_links = ['username']
    readonly_fields = ['date_joined']
    date_hierarchy = 'date_joined'
    list_filter = ['date_joined', 'is_active', 'is_staff', 'is_superuser'] #بيكون للحاجات اللي قيمها قليل
    search_fields = ['username', 'email', 'phone_number']##ينفع فيها __
