from django.db import models
from django.contrib.auth.models import User

class Container(models.Model):
    stock_name = models.CharField(max_length=100)
    stock_price = models.IntegerField()
   

    def __str__(self):
        return self.stock_name
