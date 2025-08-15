from django.db import models


class LandingPage(models.Model):
    banner_title = models.CharField(max_length=255, blank=True)
    banner_subtitle = models.CharField(max_length=500, blank=True)
    banner_image_url = models.URLField(blank=True, null=True, help_text="Paste an external image/video URL")
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Landing ({self.banner_title[:30]})" if self.banner_title else "Landing Page"



class Location(models.Model):
    location = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True, null=True, help_text="Paste an external image/video URL")

    class Meta:
        ordering = ['location']

    def __str__(self):
        return self.location
        
class Product(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
    ]

    BHK_CHOICES = [
        ('1bhk', '1 BHK'),
        ('2bhk', '2 BHK'),
        ('3bhk', '3 BHK'),
        ('4bhk', '4 BHK'),
    ]

    FURNISHING_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]

    AVAILABILITY_CHOICES = [
        ('ready', 'Ready to Move'),
        ('under_construction', 'Under Construction'),
    ]
    
    # New category choices
    CATEGORY_CHOICES = [
        ('rental', 'Rental'),
        ('property', 'Property for Sale'),
    ]

    title = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    location = models.ManyToManyField('Location', blank=True)
    description = models.TextField(blank=True, null=True)
    images_urls = models.JSONField(default=list, blank=True, null=True, help_text="List of image URLs as JSON array")
    video_url = models.URLField(blank=True, null=True, help_text="Paste video URL (YouTube, MP4, etc.)")
    
    # New fields from UI filter
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, blank=True, null=True)
    area_size = models.PositiveIntegerField(blank=True, null=True, help_text="Area size in square meters")
    bhk = models.CharField(max_length=10, choices=BHK_CHOICES, blank=True, null=True)
    furnishing = models.CharField(max_length=20, choices=FURNISHING_CHOICES, blank=True, null=True)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='property', 
                              help_text="Is this a rental property or property for sale?")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title or "Untitled Product"

    def get_images(self):
        return self.images_urls or []

    def get_video_src(self):
        return self.video_url or None

    def get_categories_list(self):
        return list(self.categories.values_list('name', flat=True))