from rest_framework import serializers
from .models import Category, Product, Unit, Banner


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name', 'short_name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'image', 'order']


class ProductSerializer(serializers.ModelSerializer):
    unit = UnitSerializer(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price',
            'image', 'is_active', 'unit', 'category', 'category_name', 'created_at'
        ]


class BannerSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Banner
        fields = [
            'id', 'title', 'subtitle', 'tag', 'image', 'image_url',
            'button_text', 'link', 'category', 'category_name', 'is_active', 'order'
        ]


