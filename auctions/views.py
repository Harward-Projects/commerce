from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import User, Listings, Bids, Comments, Categories


def index(request):
    Active_Listings = Listings.objects.all()
    return render(request, "auctions/index.html", {
        "list": Active_Listings,
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
        category_name = request.POST.get("category")
        comment_text = request.POST.get("comment")
        user = request.user.username
        
        #Checks if title is blank or repetitive
        if title:
            if Listings.objects.filter(title=title).exists():
                return render(request, "auctions/create_listing.html", {
                    "message": "Title repetitve, please select another title."
                })
        else:
            return render(request, "auctions/create_listing.html", {
                "message": "Enter the title ."
            })
        
        # Checks if Bid is blank or repetitive
        if bid_price:
            bid, created_bid = Bids.objects.get_or_create(bid_price=bid_price)
        else:
            return render(request, "auctions/create_listing.html", {
                "message": "Enter bid price."
            })

        # Checks if Category is blank or repetitive
        if category_name:
            category, created_category = Categories.objects.get_or_create(name=category_name)
        else:
            category, created_category = Categories.objects.get_or_create(name="Uncategorized")
        
        #Checks if comment is blank or repetitive
        if comment_text:
            comment, created_comment = Comments.objects.get_or_create(content=comment_text)
        else:
            comment, created_comment = Comments.objects.get_or_create(content="No comment")
            # comment.save()
        
        listing = Listings(title=title, description=description, photo_url=photo_url, comment=comment, user=user)
        listing.save()
            
        print("Listing saved and redirecting...")

        # listing.bid_price.add(bid)
        # listing.category.add(category)

        Active_Listings = Listings.objects.all()
        return render(request, "auctions/index.html", {
            "list": Active_Listings,
            # "listing": listing,
            # "message": "Fields saved correctly.",
            # "bid": bid.bid_price,
            # "title":listing.title,
            # "category":category.name,
            # "listing category": listing.category,
        })
    else:
        print("Why else?")
        return render(request, "auctions/create_listing.html")

def listing(request, title):
    listing = get_object_or_404(Listings, title=title)
    return render(request, "auctions/listing.html", {
        "item": listing,
    })