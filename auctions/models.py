from django.contrib.auth.models import AbstractUser
from django.db import models

class Bids(models.Model):
    bid_price = models.DecimalField(decimal_places=2, max_digits=6)

    def __str__(self):
        return str(self.bid_price)

class Comments(models.Model):
    content = models.TextField(blank=True)
    # title = models.ForeignKey('Listings', on_delete=models.CASCADE, related_name="comments_title")
    user = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.content


class Categories(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class User(AbstractUser):
    pass


class Listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=100)
    photo_url = models.URLField(max_length=300, blank=True)
    category = models.ManyToManyField(Categories, blank=True, related_name="Category")
    # There must be an optional base_price and bid_price. The final price should be max of these base and bid prices.
    prices = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    bid_price = models.ManyToManyField(Bids, related_name="Bid_price")
    # date = models.DateTimeField()
    comments = models.ManyToManyField(Comments, blank=True, related_name="listings")
    active_state = models.BooleanField(default=True, null=True)
    user = models.CharField(max_length=64, blank=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name='added_listings')

