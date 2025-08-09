from django.views.generic import TemplateView, DetailView, View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from .models import LandingPage, Product


class LandingView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['landing'] = LandingPage.objects.first()
        ctx['products'] = Product.objects.all()[:9]
        return ctx


class PropertyListView(TemplateView):
    template_name = 'property_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['locations'] = Product.objects.values_list('location', flat=True).distinct()
        ctx['properties'] = Product.objects.all()[:12]  
        return ctx


class PropertyFilterAjaxView(View):
    def get(self, request, *args, **kwargs):
        qs = Product.objects.all()
        location = request.GET.get('location')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        q = request.GET.get('q')

        if request.GET.get('city'):
            qs = qs.filter(city=request.GET['city'])

        if location:
            qs = qs.filter(location__icontains=location)
        if min_price:
            try:
                qs = qs.filter(price__gte=float(min_price))
            except ValueError:
                pass
        if max_price:
            try:
                qs = qs.filter(price__lte=float(max_price))
            except ValueError:
                pass
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))

        html = render_to_string('_property_cards.html', {'properties': qs}, request=request)
        return JsonResponse({'html': html, 'count': qs.count()})


class PropertyDetailView(DetailView):
    model = Product
    template_name = 'property_detail.html'
    context_object_name = "property"
