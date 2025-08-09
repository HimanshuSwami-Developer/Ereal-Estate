from django.contrib import admin
from .models import LandingPage, Location, Product, Category, Size, ProductSize

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1
    fields = ('size', 'quantity', 'price_modifier')
    show_change_link = True

@admin.register(LandingPage)
class LandingPageAdmin(admin.ModelAdmin):
    list_display = ('banner_title', 'updated')
    fieldsets = (
        (None, {
            'fields': ('banner_title', 'banner_subtitle', 'banner_image_url')
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('location',)
    search_fields = ('location',)
   
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'get_location', 'created_at', 'updated_at')  # Changed to use method
    search_fields = ('title', 'location__location', 'description')
    list_filter = ('location', 'categories', 'created_at')
    filter_horizontal = ('categories',)  # Removed 'sizes' from here
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProductSizeInline]  # Manage sizes through the inline
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'price', 'location')
        }),
        ('Media', {
            'fields': ('images_urls', 'video_url'),
            'classes': ('collapse',)
        }),
        ('Classification', {
            'fields': ('categories',),  # Removed 'sizes' from here
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_location(self, obj):
        return obj.location.location if obj.location else "-"
    get_location.short_description = 'Location'
    get_location.admin_order_field = 'location__location'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('location').prefetch_related('categories')