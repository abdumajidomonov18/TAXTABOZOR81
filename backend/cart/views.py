from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from catalog.models import Product
from .models import Cart, CartItem
from .serializers import CartSerializer


def get_user_and_cart(telegram_id):
    """Helper: telegram_id bo'yicha user va uning savatini olish."""
    try:
        user = User.objects.get(telegram_id=telegram_id)
        cart, _ = Cart.objects.get_or_create(user=user)
        return user, cart, None
    except User.DoesNotExist:
        return None, None, 'Foydalanuvchi topilmadi'


class CartView(APIView):
    """
    GET /api/cart/?telegram_id=123
    Foydalanuvchi savatini mahsulotlar bilan birga qaytarish.
    """
    def get(self, request):
        telegram_id = request.query_params.get('telegram_id')
        if not telegram_id:
            return Response({'error': 'telegram_id parametri kerak'}, status=status.HTTP_400_BAD_REQUEST)

        user, cart, error = get_user_and_cart(telegram_id)
        if error:
            return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)

        return Response(CartSerializer(cart).data)


class CartAddView(APIView):
    """
    POST /api/cart/add/
    Body: { "telegram_id": 123, "product_id": 5, "quantity": 2 }
    Savatga mahsulot qo'shish. Agar bor bo'lsa — miqdorni oshirish.
    """
    def post(self, request):
        telegram_id = request.data.get('telegram_id')
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        if not telegram_id or not product_id:
            return Response(
                {'error': 'telegram_id va product_id kerak'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if quantity < 1:
            return Response({'error': 'Miqdor 1 dan kam bo\'lmasligi kerak'}, status=status.HTTP_400_BAD_REQUEST)

        user, cart, error = get_user_and_cart(telegram_id)
        if error:
            return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)

        try:
            product = Product.objects.get(pk=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response({'error': 'Mahsulot topilmadi'}, status=status.HTTP_404_NOT_FOUND)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


class CartRemoveView(APIView):
    """
    POST /api/cart/remove/
    Body: { "telegram_id": 123, "product_id": 5, "quantity": 1 }
    Savatdan miqdorni kamaytirish. Miqdor 0 ga tushsa — element o'chiriladi.
    quantity=0 yuborilsa — to'liq o'chiriladi.
    """
    def post(self, request):
        telegram_id = request.data.get('telegram_id')
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        if not telegram_id or not product_id:
            return Response({'error': 'telegram_id va product_id kerak'}, status=status.HTTP_400_BAD_REQUEST)

        user, cart, error = get_user_and_cart(telegram_id)
        if error:
            return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)

        try:
            item = CartItem.objects.get(cart=cart, product_id=product_id)
        except CartItem.DoesNotExist:
            return Response({'error': 'Mahsulot savatda yo\'q'}, status=status.HTTP_404_NOT_FOUND)

        if quantity == 0 or item.quantity <= quantity:
            item.delete()
        else:
            item.quantity -= quantity
            item.save()

        return Response(CartSerializer(cart).data)


class CartClearView(APIView):
    """
    POST /api/cart/clear/
    Body: { "telegram_id": 123 }
    Savatni to'liq tozalash (buyurtma berilgandan keyin chaqiriladi).
    """
    def post(self, request):
        telegram_id = request.data.get('telegram_id')
        if not telegram_id:
            return Response({'error': 'telegram_id kerak'}, status=status.HTTP_400_BAD_REQUEST)

        user, cart, error = get_user_and_cart(telegram_id)
        if error:
            return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)

        cart.items.all().delete()
        return Response({'message': 'Savat tozalandi'})
