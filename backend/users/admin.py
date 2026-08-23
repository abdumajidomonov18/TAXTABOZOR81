from django.contrib import admin
from .models import User, Address


class AddressInline(admin.TabularInline):
    """User admin sahifasida manzillarni inline ko'rsatish."""
    model = Address
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'full_name', 'phone_number', 'created_at')
    search_fields = ('telegram_id', 'full_name', 'phone_number')
    readonly_fields = ('created_at',)
    inlines = [AddressInline]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'address_text', 'is_default', 'created_at')
    list_filter = ('is_default',)
    search_fields = ('user__full_name', 'user__telegram_id', 'address_text')
