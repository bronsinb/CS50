from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings")
    image = models.CharField(max_length=2000)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def current_bid(self):
        return self.bids.all().order_by('bid').last().bid

    def __str__(self):
        return f"{self.title} (${self.price})"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.bid} from @{self.bidder.username} on  {self.listing.title}"

class Comment(models.Model):
    commentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.comment} from @{self.commentor.username} on  {self.listing.item}"