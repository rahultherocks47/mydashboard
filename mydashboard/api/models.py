from django.db import models

# Create your models here.
class Stock(models.Model):
    dated = models.DateTimeField(auto_now_add=True)
    symbol = models.CharField(max_length=20)
    open = models.IntegerField(null=True)
    high = models.IntegerField(null=True)
    low = models.IntegerField(null=True)
    close = models.IntegerField(null=True)
    volume = models.IntegerField(null=True)  