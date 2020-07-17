from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    item = models.CharField(max_length=128)
    description = models.CharField(max_length=500, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item} (${self.price})"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.bid} from @{self.bidder.username} on  {self.listing.item}"

class Comment(models.Model):
    commentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.comment} from @{self.commentor.username} on  {self.listing.item}"