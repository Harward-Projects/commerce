from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

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
    print(listings_of_category)
    
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
                listing = Listings(title=title, description=description, photo_url=photo_url, user=user)
                print("listing created")
                listing.save()
                print("listing saved")
        else:
            return render(request, "auctions/create_listing.html", {
                "message": "Enter the title ."
            })
        
        # Checks if Bid is blank or repetitive
        if bid_price:
            bid, created_bid = Bids.objects.get_or_create(bid_price=bid_price)
            if created_bid:
                if Listings.objects.all():
                    print("Listings.objects.all()", Listings.objects.all())
                    # bidprice = bid.bid_price
                    listing.bid_price.set([bid])
                    # Listings.objects.filter(title=title).bid_price.add(bid)
        else:
            return render(request, "auctions/create_listing.html", {
                "message": "Enter bid price."
            })

        # Checks if Category is blank or repetitive
        if category_name:
            category, created_category = Categories.objects.get_or_create(name=category_name)
            print(category)
            ramak_listing = Listings.objects.get(title="Ramak")
            parisa_listing = Listings.objects.get(title="Parisa")
            print("Ramak category: ", ramak_listing.title)
            print("Parisa category: ", parisa_listing.description)
        else:
            category, created_category = Categories.objects.get_or_create(name="Uncategorized")

        # Now, set the categories using .set() method
        listing.category.set([category])

        #Checks if comment is blank or repetitive
        if comment_text:
            comment, created_comment = Comments.objects.get_or_create(content=comment_text, user=user)
        else:
            comment, created_comment = Comments.objects.get_or_create(content="No comment", user=user)
        
        listing.comments.set([comment])

        # listing = Listings(title=title, description=description, photo_url=photo_url, user=user)
        # listing.save()
            
        print("Listing saved and redirecting...")
        print(listing)

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

def view_listing(request, title):
    listing = get_object_or_404(Listings, title=title)
    # listing.price = listing.bid_price.
    user = request.user.username
    # user_id = User.objects.get(username=user).id
    # listing_id = Listings.objects.get(title=title).id
    
    # print(listing.watchlist.filter(Q(listings_id=listing_id) & Q(user_id=user_id)))
    # print(f"state: {listing.watchlist.filter(id=user_id).exists()} and user: {user}")
    print(f"state: {listing.watchlist.filter(username=user).exists()} and user: {user}")

    return render(request, "auctions/listing.html", {
        "item": listing,
    })