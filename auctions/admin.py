from django.contrib import admin

from .models import Listings, Categories, Comments, Bids

# Register your models here.
@admin.register(Listings)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'price', 'get_comment_list', 'user', 'creation_date']

    def get_comment_list(self, listing):
        comments = listing.comments.all()
        return ", ".join(comment.content for comment in comments)
        # return list(listing.content.values_list('content', flat=True))
    
    get_comment_list.short_description = 'comments'

@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content']

@admin.register(Bids)
class BidAdmin(admin.ModelAdmin):
    list_display = ['bid_price', 'user']