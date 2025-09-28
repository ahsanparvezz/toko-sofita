from django.forms import ModelForm
from main.models import Product
from django import forms

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "thumbnail", "category", "is_featured", "stock", "rating", "brand", "quantity"]
    
    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating is not None and (rating < 1 or rating > 5):
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating
