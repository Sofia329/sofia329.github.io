from django.contrib import admin


# Register your models here.
from .models import Condition, Category,Auction, Bid, Comment

admin.site.register(Condition)
admin.site.register(Category)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Comment)

