from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follower = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="following")

    def get_follower_count(self):
        return len(self.follower.all())
    
    def get_following_count(self):
        return len(self.following.all())


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    text = models.CharField(max_length=280)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")

    def get_likes_num(self):
        return len(self.likes.all())
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "text": self.text,
            "created": self.created.strftime("%b %-d %Y, %-I:%M %p"),
            "likes": [like.username for like in self.likes.all()]
        }