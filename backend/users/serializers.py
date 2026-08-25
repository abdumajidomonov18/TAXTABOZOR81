from rest_framework import serializers
from .models import User, Address


class AddressSerializer(serializers.ModelSerializer):
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, default=0, allow_null=True)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, default=0, allow_null=True)

    class Meta:
        model = Address
        fields = ['id', 'title', 'address_text', 'latitude', 'longitude', 'is_default', 'created_at']
        read_only_fields = ['id', 'created_at']



class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'telegram_id', 'phone_number', 'full_name', 'created_at', 'addresses']
        read_only_fields = ['id', 'created_at']


class UserRegisterSerializer(serializers.Serializer):
    """
    Foydalanuvchini ro'yxatdan o'tkazish yoki topish uchun serializer.
    get_or_create mantiqasi view'da amalga oshiriladi.
    """
    telegram_id = serializers.IntegerField()
    phone_number = serializers.CharField(max_length=20)
    full_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
