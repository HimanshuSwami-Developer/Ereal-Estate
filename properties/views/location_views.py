from properties.serializer import LocationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Location


class LocationListAPI(APIView):
    def get(self, request):
        locations = Location.objects.all()
        return Response(LocationSerializer(locations, many=True).data)
