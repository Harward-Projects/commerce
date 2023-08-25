from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=100)
    photo_url = models.URLField(max_length=300, blank=True)
    category = models.ManyToManyField('Categories', blank=True)
    # photo = models.ImageField(upload_to='images/', height_field=None, width_field=None, max_length=100)
    # There must be an optional base_price and final price should be max of the base and bid prices.
    price = models.DecimalField(decimal_places=2, max_digits=6)
    bid_price = models.ManyToManyField('Bids', blank=True, default=price)
    # date = models.DateTimeField()
    comment = models.ForeignKey('Comments', blank=True, on_delete=models.CASCADE)
    # active_state = models.BooleanField(default=False)

class Bids(models.Model):
    bid_price = models.DecimalField(decimal_places=2, max_digits=6)

class Comments(models.Model):
    content = models.TextField()

class Categories(models.Model):
    name = models.CharField(max_length=64)
