from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms

class User(AbstractUser):
    pass


# 1 list can have 1 condition only, 1 condition can appy to multiple listings
# conditions: New/Open Box/Used
class Condition(models.Model):
    condition=models.CharField(max_length=16)

    def __str__(self):
        return self.condition


# 1 listing belongs to 1 category, 1 category can apply to multiple listings
class Category(models.Model):
    category = models.CharField(max_length=16)

    def __str__(self):
        return self.category


# 1 user can have many auction listings, but 1 listing only have 1 user
class Auction(models.Model):
    image=models.URLField(blank=True, null=True)
    title = models.CharField(max_length=32)
    description = models.TextField()
    start_bid = models.DecimalField(max_digits=10, decimal_places=2) # Price is diff between auction/buy it now
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
    condition= models.ForeignKey(Condition, on_delete=models.CASCADE, related_name="auctions")
    status=models.BooleanField(default=True) # still selling or sold out
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name="auctions")
    timestamp = models.DateTimeField(auto_now_add=True)
    watcher = models.ManyToManyField(User, blank=True, related_name="watchlist")


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['image','title', 'description', 'start_bid', 'condition', 'status', 'category']


# 1 user can place multiple bids on different listings, but 1 bid can only be placed by a single user
# 1 listing can receive multiple bids, but 1 bid can only for a single listing
class Bid(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction=models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    price= models.DecimalField(max_digits=10, decimal_places=2)
    timestamp=models.DateTimeField(auto_now_add=True)

# 1 listing can have many comments, 1 comment can only be made for 1 listing
# 1 comment can only be made by 1 user, but 1 user can make many comments
class Comment(models.Model):
    auction=models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)


