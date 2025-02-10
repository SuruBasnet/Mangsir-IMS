from django.db import models
from django.contrib.auth.models import AbstractUser,Group



# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=200,null=True)
    password = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    image = models.FileField(upload_to='media/user/')
    groups = models.ForeignKey(Group,on_delete=models.SET_NULL,null=True,blank=True)
    is_active = models.BooleanField(default=False)
    otp = models.IntegerField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    stock = models.IntegerField()
    type_id = models.ForeignKey('ProductType',on_delete=models.SET_NULL,null=True)
    department_id = models.ManyToManyField('Department',blank=True)
    description = models.TextField()

class Department(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

class ProductType(models.Model):
    name = models.CharField(max_length=200)

class Purchase(models.Model):
    price = models.FloatField()
    quantity = models.IntegerField()
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    vendor_id = models.ForeignKey('Vendor',on_delete=models.CASCADE,null=True,blank=True)
    user_id = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

class Sell(models.Model):
    price = models.FloatField()
    quantity = models.IntegerField()
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200)
    user_id = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

class Vendor(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=200)
    contact_no = models.CharField(max_length=200)
    email = models.EmailField()