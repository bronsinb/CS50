from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Card(models.Model):
    name = models.CharField(max_length=128)
    number = models.CharField(max_length=16)
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return f"Card of {self.name}"

class User(AbstractUser):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="users", blank=True, null=True)

class Hotel(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    image = models.CharField(max_length=2000, default="https://sciences.ucf.edu/psychology/wp-content/uploads/sites/63/2019/09/No-Image-Available.png")

    def serialize(self):
        return {
            "name": self.name,
            "address": self.address,
            "image": self.image
        }

    def __str__(self):
        return f"{self.name}"

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    number = models.IntegerField(default=1)
    room_type = models.CharField(max_length=32, default="Single")
    image = models.CharField(max_length=2000, default="https://sciences.ucf.edu/psychology/wp-content/uploads/sites/63/2019/09/No-Image-Available.png")
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def serialize(self):
        return {
            "hotel": self.hotel.serialize(),
            "number": self.number,
            "room_type": self.room_type,
            "image": self.image,
            "price": self.price
        }

    def __str__(self):
        return f"Room at {self.hotel.name} ($${self.price})"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return f"Room for {self.user.username} from {self.start} to {self.end}"