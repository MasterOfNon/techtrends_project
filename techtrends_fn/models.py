from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category (models.Model):
    name= models.CharField(max_length=100)
    slug=models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug= slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Category name: {self.name}" 

class Product(models.Model):
    name=models.CharField(max_length=250)
    description=models.TextField()
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    slug=models.SlugField(unique=True, blank=True)
    image=models.ImageField(upload_to= 'product_images/')
    average_rating=models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    no_of_users=models.PositiveIntegerField(default=0)
    price_amazon=models.DecimalField(max_digits=10, decimal_places=2,  validators=[MinValueValidator(Decimal('0.00'))])
    price_flipkart = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
    
        super().save(*args, **kwargs)
    
    def update_average_rating(self):
        ratings=self.ratings.all()
        if ratings.exists():
            self.average_rating=sum(rating.score for rating in ratings)/ ratings.count()
            self.no_of_users=ratings.count()
        else:
            self.average_rating=0
        self.save()

    
    def __str__(self):
        return f"Product name : {self.name}" # what happends when return print (f"{self.name}")
    
class Ratings(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings' )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    score = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    class Meta: #Meta class can control how the model behaves in the database.
        unique_together= ('user', 'product')
    

    def __str__(self):
        return f"{self.user.username}'s rating for {self.product.name}: {self.score}"
    

@receiver(post_save, sender=Ratings)
def update_product_average_rating(sender, instance, **kwargs):
    instance.product.update_average_rating()


class Review(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"username : {self.user.username} has revieww for {self.product.name}"



    