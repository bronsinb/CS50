from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError

from .models import User, Hotel, Room

# Create your views here.
def index(request):
    return render(request, "hotels/index.html", {
        "type": "Rooms",
        "rooms": Room.objects.all()
    })

def hotel_rooms(request, hotel_name):
    return render(request, "hotels/index.html", {
        "type": "Rooms: " + hotel_name,
        "rooms": Room.objects.filter(hotel=(Hotel.objects.filter(name=hotel_name).first()))
    })

def hotels(request):
    return render(request, "hotels/hotels.html", {
        "hotels": Hotel.objects.all()
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
            return render(request, "hotels/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request,  "hotels/login.html")


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
            return render(request, "hotels/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "hotels/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "hotels/register.html")