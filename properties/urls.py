from django.urls import path
from . import views
app_name = 'properties' 
urlpatterns = [
    path('', views.LandingView.as_view(), name='index'),
    path('properties/', views.PropertyListView.as_view(), name='property_list'),
    path('properties/ajax-filter/', views.PropertyFilterAjaxView.as_view(), name='property_filter_ajax'),
  path('property/<int:pk>/', views.PropertyDetailView.as_view(), name='property_detail')

]
