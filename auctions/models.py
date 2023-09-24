from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class Bids(models.Model):
    bid_price = models.DecimalField(decimal_places=2, max_digits=6)
    user = models.CharField(max_length=64, default='admin')

    def __str__(self):
        return str(self.bid_price)

class Comments(models.Model):
    content = models.TextField(blank=True)

    def __str__(self):
        return self.content


class Categories(models.Model):
    name = models.CharField(max_length=64, default="Uncategorized")

    def __str__(self):
        return self.name


class User(AbstractUser):
    pass


class Listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=100)
    photo_url = models.URLField(max_length=300, blank=True)
    category = models.ManyToManyField(Categories, blank=True, related_name="Category")
    price = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    bids_number = models.IntegerField(default=0)
    bid_price = models.ManyToManyField(Bids, related_name="Bid_price")
    creation_date = models.DateTimeField(default=datetime.now())
    comments = models.ManyToManyField(Comments, blank=True, null=True, related_name="listings")
    active_state = models.BooleanField(default=True, null=True)
    user = models.CharField(max_length=64, blank=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name='added_listings')

