from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'unit', 'quantity', 'price', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    user_phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    user_telegram_id = serializers.IntegerField(source='user.telegram_id', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'status', 'status_display', 'payment_method',
            'user_full_name', 'user_phone_number', 'user_telegram_id',
            'address_text', 'latitude', 'longitude',
            'total_price', 'comment', 'items', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'total_price', 'created_at']



class OrderCreateSerializer(serializers.Serializer):
    """
    Yangi buyurtma yaratish uchun kiruvchi ma'lumotlar.
    Cart'dagi mahsulotlardan avtomatik OrderItem'lar yaratiladi.
    """
    telegram_id = serializers.IntegerField()
    address_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(
        choices=['cash', 'payme', 'click'],
        default='cash'
    )
    comment = serializers.CharField(required=False, allow_blank=True, default='')
