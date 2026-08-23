from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryListView(APIView):
    """
    GET /api/products/categories/
    Barcha faol kategoriyalar ro'yxati.
    """
    def get(self, request):
        categories = Category.objects.all()
        return Response(CategorySerializer(categories, many=True).data)


class ProductListView(APIView):
    """
    GET /api/products/
    Mahsulotlar ro'yxati. Filtrlar:
    - ?category=<id>       — kategoriya bo'yicha filter
    - ?search=<text>       — nomi bo'yicha qidirish
    - ?min_price=&max_price= — narx oralig'i
    """
    def get(self, request):
        queryset = Product.objects.filter(is_active=True).select_related('category', 'unit')

        # Kategoriya filtri
        category_id = request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Qidirish
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)

        # Narx filtri
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return Response(ProductSerializer(queryset, many=True).data)


class ProductDetailView(APIView):
    """
    GET /api/products/<id>/
    Bitta mahsulot ma'lumotlari.
    """
    def get(self, request, pk):
        try:
            product = Product.objects.select_related('category', 'unit').get(pk=pk, is_active=True)
        except Product.DoesNotExist:
            return Response({'error': 'Mahsulot topilmadi'}, status=status.HTTP_404_NOT_FOUND)

        return Response(ProductSerializer(product).data)
