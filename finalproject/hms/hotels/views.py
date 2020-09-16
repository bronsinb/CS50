import datetime
import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Hotel, Room, Booking, Card

# Create your views here.
def index(request):
    return render(request, "hotels/index.html", {
        "type": "Rooms",
        "card": Card.objects.filter(user=request.user).first()
    })

def hotel_rooms(request, hotel_name):
    return render(request, "hotels/index.html", {
        "type": "Rooms: " + hotel_name,
        "hotel": hotel_name,
        "card": Card.objects.filter(user=request.user).first()
    })

def hotels(request):
    return render(request, "hotels/hotels.html", {
        "hotels": Hotel.objects.all()
    })

def profile(request):
    return render(request, "hotels/profile.html", {
        "rooms": request.user.bookings.all(),
        "card": Card.objects.filter(user=request.user).first(),
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

@csrf_exempt
def rooms(request):
    if request.method == "POST":
        data = json.loads(request.body)
        start = datetime.date.fromisoformat(data['start'])
        end = datetime.date.fromisoformat(data['end'])
        hotel = data["hotel"]
        search = data["search"]

        rooms = Room.objects.all()

        if len(hotel) > 0:
            rooms = rooms.filter(hotel__in=(Hotel.objects.filter(name=hotel)))

        if search:
            rooms = rooms.filter(hotel__in=(Hotel.objects.filter(name__icontains=search))) | rooms.filter(hotel__in=(Hotel.objects.filter(address__icontains=search))) | rooms.filter(room_type__icontains=search) | rooms.filter(number__icontains=search) | rooms.filter(price__icontains=search)

        booked_rooms = Booking.objects.filter(start__range=(start, end)) | Booking.objects.filter(end__range=(start, end))

        rooms = rooms.exclude(pk__in=booked_rooms)
        return JsonResponse([room.serialize() for room in rooms], safe=False)

@csrf_exempt
def card(request):
    if request.method == "PUT":
        if Card.objects.filter(user=request.user).first():
            Card.objects.filter(user=request.user).first().delete()
            return JsonResponse({"status": "Removed"}, status=200)
        else:
            data = json.loads(request.body)
            Card(user=request.user, name=data["name"], number=data["cardnum"], cvv=data["cvv"], expire=data["expire"]).save()
            return JsonResponse({"status": "Added"}, status=200)