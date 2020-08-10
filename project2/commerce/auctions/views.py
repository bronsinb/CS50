from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Category, Bid, Comment

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "name": "Active Listings"
    })

def profile(request, username):
    user = User.objects.filter(username=username).first()
    if user == None:
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.all(),
            "name": "Active Listings",
            "message": "User not found."
        })

    return render(request, "auctions/profile.html", {
        "user_profile": user,
        "listings": user.listings.all()
    })

@login_required(login_url='/login')
def watchlist(request):
    return render(request, "auctions/index.html", {
        "listings": request.user.watchlists.all(),
        "name": "Watchlist"
    })

def category(request, category):
    if request.method == "POST":
        return HttpResponseRedirect(reverse("category", args=[request.POST["cat"]]))
        
    categories = Category.objects.exclude(name=category).all()
    cat = Category.objects.filter(name=category).first()

    if cat == None:
        return HttpResponseRedirect(reverse("category", args=[categories[0].name]))

    return render(request, "auctions/category.html", {
        "category": category,
        "listings": Listing.objects.filter(category=cat).all(),
        "categories": categories,
    })

def listing(request, listing_id):
    try: 
        listing = Listing.objects.get(id=listing_id)
        if request.method == "POST":
            if request.POST["action"] == "watchlist":
                if listing in request.user.watchlists.all():
                    request.user.watchlists.remove(listing)
                else:
                    request.user.watchlists.add(listing)
            if request.POST["action"] == "bid":
                Bid(bid=request.POST["price"], bidder=request.user, listing=listing).save()
            if request.POST["action"] == "comment":
                Comment(listing=listing, commentor=request.user, comment=request.POST["comment"]).save()
            if request.POST["action"] == "status":
                listing.active = (not listing.active)
                listing.save()

            return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "comments": listing.all_comments,
                    "watchlisted": listing in request.user.watchlists.all()
                })
        else: 
            if request.user.is_authenticated:
                return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "comments": listing.all_comments,
                        "watchlisted": listing in request.user.watchlists.all()
                    })
            else:
                return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "comments": listing.all_comments,
                        "watchlisted": False
                    })
    except Listing.DoesNotExist:
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.all(),
            "name": "Active Listings",
            "message": "Listing Not Found"
        })

@login_required(login_url='/login')
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        url = request.POST["image"]
        category = Category.objects.get(name=request.POST["category"])

        if url == "":
            listing = Listing(user=request.user, title=title, description=description, category=category, price=price)
        else:
            listing = Listing(user=request.user, title=title, description=description, category=category, image=url, price=price)
        
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/createlisting.html", {
                "categories": Category.objects.all()
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
        first = request.POST["firstname"]
        last = request.POST["lastname"]
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
            user.first_name = first
            user.last_name = last
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
