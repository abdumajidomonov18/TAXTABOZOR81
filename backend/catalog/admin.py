from django.contrib import admin
from .models import Category, Unit, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name', 'order')
    list_editable = ('order',)  # Tartibni to'g'ridan-to'g'ri ro'yxatdan o'zgartirish
    search_fields = ('name',)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name')
    search_fields = ('name', 'short_name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'unit', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'unit')
    list_editable = ('is_active', 'price')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    ordering = ('category', 'name')
