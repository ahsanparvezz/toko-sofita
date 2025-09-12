from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)

    # tambahan 
    stock = models.IntegerField(default=0)
    rating = models.FloatField(null=True, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    

## komentar tambahan trigger deploy