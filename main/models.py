from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

# Create your models here.

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    CATEGORY_CHOICES = [
        ('jersey', 'Jersey'),
        ('shoes', 'Football Shoes'),
        ('balls', 'Balls'),
        ('training', 'Training Equipment'),
        ('accessories', 'Accessories'),
        ('lifestyle', 'Lifestyle'),
    ]
    
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='shoes')
    is_featured = models.BooleanField(default=False)
    views = models.IntegerField(default=0)



    # tambahan 
    stock = models.IntegerField(default=0)
    rating = models.FloatField(null=True, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    quantity = models.IntegerField(default=0)


    def __str__(self):
        return self.name
    
    @property
    def is_product_hot(self):
        return self.views > 20
        
    def increment_views(self):
        self.views += 1
        self.save()

    def clean(self):
        if self.rating is not None and (self.rating < 1 or self.rating > 5):
            raise ValidationError("Rating must be between 1 and 5.")

## komentar tambahan trigger deploy