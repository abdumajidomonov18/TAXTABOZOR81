from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from users.models import User, Address
from cart.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer


class OrderCreateView(APIView):
    """
    POST /api/orders/create/
    Cart'dagi mahsulotlardan buyurtma yaratish.
    Muvaffaqiyatli yaratilgandan keyin savat tozalanadi.
    """
    @transaction.atomic  # Barchasi muvaffaqiyatli bo'lmasa — hech narsa saqlanmaydi
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        telegram_id = serializer.validated_data['telegram_id']
        address_id = serializer.validated_data['address_id']
        payment_method = serializer.validated_data['payment_method']
        comment = serializer.validated_data.get('comment', '')

        # User tekshirish
        try:
            user = User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            return Response({'error': 'Foydalanuvchi topilmadi'}, status=status.HTTP_404_NOT_FOUND)

        # Manzil tekshirish
        try:
            address = Address.objects.get(pk=address_id, user=user)
        except Address.DoesNotExist:
            return Response({'error': 'Manzil topilmadi'}, status=status.HTTP_404_NOT_FOUND)

        # Savat tekshirish
        try:
            cart = Cart.objects.prefetch_related('items__product__unit').get(user=user)
        except Cart.DoesNotExist:
            return Response({'error': 'Savat topilmadi'}, status=status.HTTP_404_NOT_FOUND)

        cart_items = cart.items.all()
        if not cart_items:
            return Response({'error': 'Savat bo\'sh'}, status=status.HTTP_400_BAD_REQUEST)

        # Jami narxni hisoblash
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        # Order yaratish
        order = Order.objects.create(
            user=user,
            address=address,
            address_text=address.address_text,
            latitude=address.latitude,
            longitude=address.longitude,
            total_price=total_price,
            payment_method=payment_method,
            comment=comment,
        )

        # OrderItem'larni yaratish (snapshot)
        order_items = [
            OrderItem(
                order=order,
                product=item.product,
                product_name=item.product.name,   # snapshot
                unit=item.product.unit,            # snapshot
                quantity=item.quantity,
                price=item.product.price,          # snapshot
            )
            for item in cart_items
        ]
        OrderItem.objects.bulk_create(order_items)

        # Savatni tozalash
        cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderListView(APIView):
    """
    GET /api/orders/?telegram_id=123
    Foydalanuvchi buyurtmalari tarixi (yangilardan eskiga).
    """
    def get(self, request):
        telegram_id = request.query_params.get('telegram_id')
        if not telegram_id:
            return Response({'error': 'telegram_id kerak'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            return Response({'error': 'Foydalanuvchi topilmadi'}, status=status.HTTP_404_NOT_FOUND)

        orders = Order.objects.filter(user=user).prefetch_related('items__product', 'items__unit')
        return Response(OrderSerializer(orders, many=True).data)


class OrderDetailView(APIView):
    """
    GET /api/orders/<id>/
    Bitta buyurtma tafsilotlari.
    """
    def get(self, request, pk):
        try:
            order = Order.objects.prefetch_related('items__product', 'items__unit').get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Buyurtma topilmadi'}, status=status.HTTP_404_NOT_FOUND)

        return Response(OrderSerializer(order).data)
