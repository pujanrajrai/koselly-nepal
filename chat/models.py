from django.db import models

# Create your models here.
from accounts.models import MyUser


class Chat(models.Model):
    send_from = models.ForeignKey(MyUser, on_delete=models.PROTECT,related_name='send_from')
    send_to = models.ForeignKey(MyUser, on_delete=models.PROTECT,related_name='send_to')
    message = models.CharField(max_length=1000)
    send_date_time = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)




