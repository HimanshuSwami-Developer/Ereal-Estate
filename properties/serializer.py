from rest_framework import serializers
from .models import LandingPage, Location, Product


class LandingPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPage
        fields = "__all__"



class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

