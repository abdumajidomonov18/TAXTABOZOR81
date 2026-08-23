from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Address
from .serializers import UserSerializer, UserRegisterSerializer, AddressSerializer


class UserRegisterView(APIView):
    """
    POST /api/users/register/
    Foydalanuvchini ro'yxatdan o'tkazish yoki mavjudini qaytarish.
    Bot /start komandasida telefon raqam olgandan keyin chaqiriladi.
    """
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        telegram_id = serializer.validated_data['telegram_id']
        phone_number = serializer.validated_data['phone_number']
        full_name = serializer.validated_data.get('full_name', '')

        user, created = User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={'phone_number': phone_number, 'full_name': full_name}
        )

        # Agar user allaqachon bor bo'lsa, lekin ismi yangilangan bo'lsa
        if not created and full_name and not user.full_name:
            user.full_name = full_name
            user.save(update_fields=['full_name'])

        response_data = UserSerializer(user).data
        http_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(response_data, status=http_status)


class UserDetailView(APIView):
    """
    GET /api/users/me/?telegram_id=123
    Foydalanuvchi ma'lumotlarini va manzillarini qaytarish.
    """
    def get(self, request):
        telegram_id = request.query_params.get('telegram_id')
        if not telegram_id:
            return Response(
                {'error': 'telegram_id parametri kerak'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.prefetch_related('addresses').get(telegram_id=telegram_id)
        except User.DoesNotExist:
            return Response({'error': 'Foydalanuvchi topilmadi'}, status=status.HTTP_404_NOT_FOUND)

        return Response(UserSerializer(user).data)


class AddressListCreateView(APIView):
    """
    GET  /api/users/addresses/?telegram_id=123  — Barcha manzillar
    POST /api/users/addresses/?telegram_id=123  — Yangi manzil qo'shish
    """
    def get_user(self, telegram_id):
        try:
            return User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            return None

    def get(self, request):
        telegram_id = request.query_params.get('telegram_id')
        if not telegram_id:
            return Response({'error': 'telegram_id parametri kerak'}, status=status.HTTP_400_BAD_REQUEST)

        user = self.get_user(telegram_id)
        if not user:
            return Response({'error': 'Foydalanuvchi topilmadi'}, status=status.HTTP_404_NOT_FOUND)

        addresses = user.addresses.all().order_by('-is_default', '-created_at')
        return Response(AddressSerializer(addresses, many=True).data)

    def post(self, request):
        telegram_id = request.query_params.get('telegram_id')
        if not telegram_id:
            return Response({'error': 'telegram_id parametri kerak'}, status=status.HTTP_400_BAD_REQUEST)

        user = self.get_user(telegram_id)
        if not user:
            return Response({'error': 'Foydalanuvchi topilmadi'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AddressSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        address = serializer.save(user=user)
        return Response(AddressSerializer(address).data, status=status.HTTP_201_CREATED)


class AddressDeleteView(APIView):
    """
    DELETE /api/users/addresses/<id>/
    Manzilni o'chirish.
    """
    def delete(self, request, pk):
        try:
            address = Address.objects.get(pk=pk)
        except Address.DoesNotExist:
            return Response({'error': 'Manzil topilmadi'}, status=status.HTTP_404_NOT_FOUND)

        address.delete()
        return Response({'message': 'Manzil o\'chirildi'}, status=status.HTTP_200_OK)
