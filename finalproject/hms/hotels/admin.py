from django.contrib import admin
from .models import User, Hotel, Room, Card

# Register your models here.
admin.site.register(User)
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Card)