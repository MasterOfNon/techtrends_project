from django.contrib import admin # to get the tables in admin site u need to import all the model classes here
from .models import Product, Category, Ratings, Review

# Register your models here to be displayed in admin site.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Ratings)
admin.site.register(Review)


