from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
from accounts.models import MyUser


class ProductCategories(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Season(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    user=models.ForeignKey(MyUser,on_delete=models.PROTECT,null=True,blank=True)
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    categories = models.ForeignKey(ProductCategories, on_delete=models.PROTECT)
    photo = models.ImageField(upload_to='products')
    desc = RichTextField()
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, blank=True, null=True)
    stock = models.PositiveIntegerField()
    create_date = models.DateField(auto_now=True)
    total_click = models.PositiveIntegerField(default=0)
    discount_amt = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ProductComment(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    comment = models.CharField(max_length=100)
