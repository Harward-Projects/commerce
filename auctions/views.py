from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from decimal import Decimal
from datetime import datetime

from .models import User, Listings, Bids, Comments, Categories


def index(request):
    Active_Listings = Listings.objects.filter(active_state=True)
    return render(request, "auctions/index.html", {
        "list": Active_Listings,
    })

def closed(request):
    Closed_Listings = Listings.objects.filter(active_state=False)
    return render(request, "auctions/closed_listings.html", {
        "list": Closed_Listings,
    })

def categories(request):
    categories = Categories.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories,
    })

def view_category(request, category):
    category_id = get_object_or_404(Categories, name=category).id
    listings_of_category = Listings.objects.filter(category=category_id)
    return render(request, "auctions/category.html", {
        "category": category,
        "listings_of_category": listings_of_category,

    })

def watchlist(request):
    user = request.user.username
    user_id = User.objects.get(username=user).id
    watchlist = Listings.objects.filter(watchlist=user_id)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist,
    })

def ARWatchlist(request, key, title):
    user = request.user.username
    user_id = User.objects.get(username=user).id
    listing = Listings.objects.get(title=title)
    watchlist = Listings.objects.filter(watchlist=user_id)


    # alarm message to confirm removal
    if key == 2:
        return render(request, 'auctions/listing.html', {
            "message": "You are going to remove this listing from your watchlish, are you sure?",
            "watchlist": watchlist,
            # listing in the below line represents used item in other htmls, this time listing is used to distinguish with below item in for loop!
            "item": listing,
        })
    
    # No message, first attempt to remove
    if key == 0:
        listing.watchlist.remove(user_id)
        return render(request, 'auctions/watchlist.html', {
            "message": " removed from your watchlist!",
            "watchlist": watchlist,
            "listing": listing,
        })
    
    # Adding to watchlist
    if key == 1:
        listing.watchlist.set([user_id])
        return render(request, 'auctions/watchlist.html', {
            "message": " has been added to your watchlist.",
            "watchlist": watchlist,
            "listing": listing,
        })

def add_comment_or_bid(request, title):
    listing = Listings.objects.get(title=title)
    user = request.user.username

    if request.method == 'POST':
        if 'comment_submit' in request.POST:
            new_comment = request.POST.get("new_comment")
            if new_comment:
                added_comment, created_added_comment = Comments.objects.get_or_create(content=new_comment)
                if created_added_comment:
                    listing.comments.add(added_comment.id)
                    print(f"comment added to {listing.title} listing")
                    return render(request, "auctions/listing.html", {
                            "item": listing,
                        })
                else:
                    return render(request, "auctions/listing.html", {
                        "message": "Can't add repetitive comment!",
                        "item": listing,
                    })    
            else:
                return render(request, "auctions/listing.html", {
                    "message": "Can't add empty comment!",
                    "item": listing,
                })
        elif 'bid_submit' in request.POST:
            if request.POST.get("bid"):
                try:
                    new_bid = Decimal(request.POST.get("bid"))
                except ValueError:
                    return HttpResponse("Invalid decimal: {new_bid}")
            else:
                return render(request, "auctions/listing.html", {
                    "message": "Can't put empty bid!",
                    "item": listing,
                })
            if not listing.price:
                listing.price = 0
            if new_bid > Decimal(listing.price):
                listing.price = new_bid
                listing.save()
                new_bid_record = Bids.objects.create(bid_price=new_bid, user=user)
                listing.bid_price.add(new_bid_record.id)
                listing.bids_number += 1
                listing.save()
                return render(request, "auctions/listing.html", {
                    "item": listing,
                })
            else:
                return render(request, "auctions/listing.html", {
                        "message": "You should bid a valid price greater than others'",
                        "item": listing,
                    })
        elif 'bid_close' in request.POST:
            listing.active_state = False
            listing.save()
            return render(request, "auctions/listing.html", {
                "message": "You should bid a valid price greater than others'",
                "item": listing,
            })
    else:
        return render(request, "auctions/listing.html", {
            "item": listing,
        })
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        bid_price = request.POST.get("bid_price")
        photo_url = request.POST.get("image_URL")
        category_input = request.POST.get("category")
        comment_text = request.POST.get("comment")
        user = request.user.username
        creation_date = datetime.now()
        
        #Checks if title is blank or repetitive
        if title and bid_price and description:
            if Listings.objects.filter(title=title).exists():
                return render(request, "auctions/create_listing.html", {
                    "message": "Title repetitve, please select another title."
                })
            else:
                listing = Listings(title=title, description=description, photo_url=photo_url, user=user, creation_date=creation_date)
                print("listing created")
                bid = Bids.objects.create(bid_price=bid_price, user=user)
                listing.price = bid.bid_price
                listing.save()
                print("listing saved")
        else:
            return render(request, "auctions/create_listing.html", {
                "message": "Title, description and starting bid price are mandatory."
            })
        
        # Checks if Category is blank or repetitive
        if category_input:
            categories = [category.strip() for category in category_input.split(',')]
            print(f"Category must not be Uncategorized. But is: {categories}")
            for category_name in categories:
                category, created_category = Categories.objects.get_or_create(name=category_name)
                listing.category.add(category.id)
        else:
            category, created_category = Categories.objects.get_or_create(name="Uncategorized")
            listing.category.add(category.id)

        #Checks if comment is blank or repetitive
        if comment_text:
            comment, created_comment = Comments.objects.get_or_create(content=comment_text)
        else:
            comment, created_comment = Comments.objects.get_or_create(content="No comment")
        listing.comments.add(comment.id)
        Active_Listings = Listings.objects.all()

        return render(request, "auctions/index.html", {
            "list": Active_Listings,
        })
    else:
        return render(request, "auctions/create_listing.html")

def view_listing(request, title):
    listing = get_object_or_404(Listings, title=title)
    return render(request, "auctions/listing.html", {
        "item": listing,
        })
