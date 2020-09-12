from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass


#class Card(models.Model):
 #   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cards")
  #  number = models.CharField()

class Hotel(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    image = models.CharField(max_length=2000, default="https://sciences.ucf.edu/psychology/wp-content/uploads/sites/63/2019/09/No-Image-Available.png")

    def __str__(self):
        return f"{self.name}"

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    number = models.IntegerField(default=1)
    room_type = models.CharField(max_length=32, default="Single")
    image = models.CharField(max_length=2000, default="https://sciences.ucf.edu/psychology/wp-content/uploads/sites/63/2019/09/No-Image-Available.png")
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Room at {self.hotel.name} ($${self.price})"