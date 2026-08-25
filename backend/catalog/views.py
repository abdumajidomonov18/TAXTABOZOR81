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


from django.db.models import Q


class ProductListView(APIView):
    """
    GET /api/products/
    Mahsulotlar ro'yxati. Filtrlar:
    - ?category=<id>       — kategoriya bo'yicha filter
    - ?search=<text>       — nomi, tavsifi va kategoriyasi bo'yicha aqlli qidirish
    - ?min_price=&max_price= — narx oralig'i
    """
    def get(self, request):
        queryset = Product.objects.filter(is_active=True).select_related('category', 'unit')

        # Kategoriya filtri
        category_id = request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Aqlli va tezkor qidirish
        search = request.query_params.get('search')
        if search:
            search = search.strip()
            words = [w for w in search.split() if len(w) > 0]
            search_query = Q()

            for word in words:
                clean_w = word.replace("'", "").replace("`", "").replace("‘", "").replace("’", "").replace("ʻ", "")
                word_q = (
                    Q(name__icontains=word) |
                    Q(description__icontains=word) |
                    Q(category__name__icontains=word)
                )
                if clean_w:
                    word_q |= (
                        Q(name__icontains=clean_w) |
                        Q(description__icontains=clean_w) |
                        Q(category__name__icontains=clean_w)
                    )
                    # "yogoch" -> "yog'och", "yo'g'och", "taxta"
                    if "o" in clean_w:
                        word_q |= Q(name__icontains=clean_w.replace("o", "o'")) | Q(category__name__icontains=clean_w.replace("o", "o'"))
                    if "g" in clean_w:
                        word_q |= Q(name__icontains=clean_w.replace("g", "g'")) | Q(category__name__icontains=clean_w.replace("g", "g'"))

                search_query &= word_q

            queryset = queryset.filter(search_query).distinct()

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
