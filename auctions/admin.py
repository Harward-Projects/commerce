from django.contrib import admin

from .models import Listings, Categories, Comments, Bids

# Register your models here.
@admin.register(Listings)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'comment']

@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content']

@admin.register(Bids)
class BidAdmin(admin.ModelAdmin):
    list_display = ['bid_price']