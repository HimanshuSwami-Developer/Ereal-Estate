from properties.serializer import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from ..models import Product


class ProductListAPI(APIView):
    def get(self, request):
        queryset = Product.objects.all()

        # Filtering manually
        location = request.GET.get('location')
        search = request.GET.get('search')

        if location:
            queryset = queryset.filter(location__id=location)
        if search:
            queryset = queryset.filter(title__icontains=search) | queryset.filter(description__icontains=search)

        return Response(ProductSerializer(queryset.distinct(), many=True).data)


class ProductDetailAPI(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(ProductSerializer(product).data)
