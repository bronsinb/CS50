from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follower = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name="followers")

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    text = models.CharField(max_length=280)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")

    def get_likes_num(self):
        return len(self.likes.all())