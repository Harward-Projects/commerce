from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
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

def create_listing(requst):
    if requst.method == "POST":
        title = requst.POST.get("title")
        description = requst.POST.get("description")
        bid_price = requst.POST.get("bid_price")
        photo_url = requst.POST.get("image_URL")
        category_name = requst.POST.get("category")
        comment_text = requst.POST.get("comment")
        print(comment_text)
        # Check if Category already exists with the same name
        category, created_category = Categories.objects.get_or_create(name=category_name)
        if created_category is True:
            category = Categories(name=category_name)
            category.save()
        # category = Categories.objects.create(name=category_name)

        # bid = Bids.objects.create(bid_price=bid_price)
        bid, created_bid = Bids.objects.get_or_create(bid_price=bid_price)
        if created_bid is True:
            bid = Bids(bid_price=bid_price)
            bid.save()
        # Check if Bid already exists with the same amount
        
        # comment = Comments.objects.create(content=comment_text)
        comment = Comments(content=comment_text)
        comment.save()
        
        listing = Listings(title=title, description=description, photo_url=photo_url, comment=comment)
        listing.save()
        
        listing.bid_price.add(bid)
        listing.category.add(category)
        
        return render(requst, "auctions/index.html", {
            "listing": listing,
            # "message": "Fields saved correctly.",
            # "bid": bid.bid_price,
            # "title":listing.title,
            # "category":category.name,
            # "listing category": listing.category,
        })
    else:
        return render(requst, "auctions/create_listing.html")
