from django.db import models

# Create your models here.


# Create your models here.
from accounts.models import MyUser


class Gender(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profiles')
    full_name = models.CharField(max_length=100)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    dob = models.DateField()
    phone_number = models.CharField(max_length=10)
    default_shipping_address = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user} {self.full_name}"

