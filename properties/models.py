from django.db import models

class LandingPage(models.Model):
    banner_title = models.CharField(max_length=255, blank=True)
    banner_subtitle = models.CharField(max_length=500, blank=True)
    banner_image_url = models.URLField(blank=True, null=True, help_text="Paste an external image/video URL")
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Landing ({self.banner_title[:30]})"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True, null=True, help_text="Paste an external image/video URL")
   
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Location(models.Model):
    location = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True, null=True, help_text="Paste an external image/video URL")
   
    class Meta:
        verbose_name_plural = "Location"
        ordering = ['location']
    
    def __str__(self):
        return self.location

class Size(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    location = models.ManyToManyField(Location, blank=True)
    description = models.TextField(blank=True)
    images_urls = models.JSONField(
        default=list,
        blank=True,
        help_text="List of image URLs as JSON array"
    )
    video_url = models.URLField(blank=True, null=True, help_text="Paste video URL (YouTube, MP4, etc.)")
    categories = models.ManyToManyField(Category, blank=True)
    sizes = models.ManyToManyField(Size, through='ProductSize', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_images(self):
        """Returns list of image URLs or empty list"""
        return self.images_urls if self.images_urls else []

    def get_video_src(self):
        return self.video_url if self.video_url else None

    def get_categories_list(self):
        return list(self.categories.values_list('name', flat=True))

    def get_available_sizes(self):
        return self.productsize_set.filter(quantity__gt=0).select_related('size')

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price_modifier = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        default=0,
        help_text="Additional price for this size (can be negative)"
    )

    class Meta:
        unique_together = ('product', 'size')
        verbose_name = "Product Size Availability"
        verbose_name_plural = "Product Size Availabilities"

    def __str__(self):
        return f"{self.product.title} - {self.size.name}"

    def get_final_price(self):
        return self.product.price + self.price_modifier