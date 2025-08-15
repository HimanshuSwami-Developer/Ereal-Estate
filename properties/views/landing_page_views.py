
from rest_framework.views import APIView
from rest_framework.response import Response
from properties.serializer import LandingPageSerializer, LocationSerializer, ProductSerializer
from properties.models import LandingPage, Location, Product

class LandingPageAPI(APIView):
    def get(self, request):
        landing = LandingPage.objects.first()
        products = Product.objects.all()[:9]
        locations = Location.objects.all()
        return Response({
            'landing': LandingPageSerializer(landing).data if landing else None,
            'products': ProductSerializer(products, many=True).data,
            'locations': LocationSerializer(locations, many=True).data
        })
