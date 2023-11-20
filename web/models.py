from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    oldPrice = models.IntegerField()
    image = models.ImageField(upload_to="media") 
    imageBack = models.ImageField(upload_to="media")       

    def __str__(self):
        return self.name
    
class Compare(models.Model):
    image = models.ImageField(upload_to='media/compare')
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField()
    stock = models.CharField(max_length=20)
    weight = models.DecimalField(verbose_name='gram', decimal_places=2, max_digits=5)
    dimension = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Wishlist(models.Model):
    image = models.ImageField(upload_to='media/wishlist')
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    stock = models.CharField(max_length=20)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
         return self.name

class OrderItem(models.Model):
     order = models.ForeignKey(Order,on_delete=models.CASCADE)
     image = models.ImageField(upload_to="media/Order_image") 
     product = models.CharField(max_length=50)
     quantity = models.IntegerField()
     price = models.FloatField()
     total = models.FloatField()

     def __str__(self):
          return f"{self.product} - {self.quantity}"