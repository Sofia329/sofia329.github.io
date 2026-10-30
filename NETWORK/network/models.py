from django.contrib.auth.models import AbstractUser
from django.db import models


# 1 user can have many followers, 1 follower can follow multiple users
# if user don;t follow anyone, or no followers, blank = True
# user A follows B, B is following A; disable symmetrical
class User(AbstractUser):
    followers = models.ManyToManyField("User",  symmetrical=False, blank= True, related_name="following")



# every post only have 1 poster/user, but 1 user can post many posts
class Post(models.Model):
    poster = models.ForeignKey("User", on_delete=models.CASCADE, related_name = "posts")
    content = models.TextField(blank=True)
    likes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "content": self.content,
            "likes": self.likes,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }