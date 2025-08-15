from django.urls import path
from properties.views.landing_page_views import LandingPageAPI
from properties.views.location_views import LocationListAPI
from properties.views.product_views import ProductListAPI, ProductDetailAPI

from properties.views.render_views import RenderHTMLPages

app_name = 'properties'


urlpatterns = [
    path("landing-page/", LandingPageAPI.as_view(), name="landing-page"),

   
    path("locations/", LocationListAPI.as_view(), name="location-list"),
    path("products/", ProductListAPI.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetailAPI.as_view(), name="product-detail"),

   
     path('<str:page_name>/', RenderHTMLPages(), name='render-page'),
     path('', RenderHTMLPages(), name='home'),

     
]
