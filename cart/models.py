from django.db import models

# Create your models here.
from accounts.models import MyUser
from products.models import Product


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    is_bought = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    order_id = models.CharField(max_length=100, null=True, blank=True)
    shipping_address = models.CharField(max_length=100, null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    is_send = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.price = self.quantity * self.product.price
        super(Cart, self).save(*args, **kwargs)
