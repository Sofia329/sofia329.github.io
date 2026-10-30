from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from decimal import Decimal
from .models import Condition, Category, User, Auction, Bid, Comment, AuctionForm


"""hardcoded values in admin for selection dropdown 
CONDITION =["New","Open Box","Used"]
CATEGORY = ["Electronics","Fashion", "Home","Toys","Sports", "Motors", "Collectibles", "Books","Business", "Other"]
"""

def index(request):
    # showing active listing re-rendered by categories
    if request.method == "POST":
        category = Category.objects.get(category = request.POST.get("category"))
        return render(request, "auctions/index.html", {
                    "auctions": Auction.objects.filter(status=True, category = category)
                })

    else:
        return render(request, "auctions/index.html", {
            "auctions": Auction.objects.filter(status=True)
        })


@login_required
def listpage(request, listpage):
    auction = Auction.objects.get(pk=listpage)
    watchlist_exist = auction in request.user.watchlist.all()
    comment = auction.comments.all()
    # chekc if the current login user is the listing creator
    owner = True if request.user == auction.user else False 

    if request.method =="GET":
        # if the auction has closed, determine winner, and if winner is current logged in user
        if auction.status == False:
            bid = auction.bids.order_by("-price").first()
            winner = bid.user if bid else None
            seller = auction.user
            if (winner == request.user) and (winner != seller):
                return render(request, "auctions/listpage.html",{
                    "auction": auction,
                    "watchlist_exist":  watchlist_exist,
                    "comments": comment,
                    "owner": owner,
                    "winner": "You have won this Auction!"
                })

        return render(request, "auctions/listpage.html", {
            "auction": auction,
            "watchlist_exist": watchlist_exist,
            "comments": comment,
            "owner": owner,
            
        })

    # listpage.html will send by post, there are three forms need to different treated
    if request.method=="POST":

        # bid price submitted by post
        if "start_bid" in request.POST:

            bid_price = Decimal(request.POST.get("start_bid"))
            # get the current max bid from the bid table, if no available bids then use start_bid
            max_bid= auction.bids.order_by("-price").first()
            max_bid_price = max_bid.price if max_bid else None

            """
            The logic placed on bid price will ensure that first check the bid price cannot be lower than start_bid price
            And then if there is existing bids available on this listing, select the highest one, and the bid price cannot be lower or equal to the current max bid
            if no existing bids available on this listing then it can place the bid price as minimal as the start_bid
            """

            if bid_price < auction.start_bid:
                messages.error(request, "Bid Price have to be at least as large as the starting bid")
                return HttpResponseRedirect(reverse("listpage", args=(listpage,))) # -> use message to shorten the lines of code to render listpage.html and passing variables and the specific messages
 
    
            elif max_bid_price is not None and bid_price <= max_bid_price:
                messages.error(request, "Bid Price have to be greater than current Max Bid Price")
                return HttpResponseRedirect(reverse("listpage", args=(listpage,)))

            else:
                # bid price is available, and save in the Bid table
                Bid.objects.create(
                    user=request.user,
                    auction=auction,
                    price=bid_price,
                )
                messages.success(request, "Bid Placed Successfully")
                return HttpResponseRedirect(reverse("listpage", args=(listpage,)))
            
        
        # toggle around "add watchlist"  and "remove watchlist" button on listpage
        
        elif "auction" in request.POST:
            
            if watchlist_exist:
                request.user.watchlist.remove(auction)
                message = "Successfully Removed from Watchlist"
            else:
                request.user.watchlist.add(auction)
                message = "Successfully Added from Watchlist"

            watchlist_exist = auction in request.user.watchlist.all()

            return render(request, "auctions/listpage.html", { 
                "auction": auction,
                "watchlist_exist":  watchlist_exist,
                "comments": comment,
                "owner": owner,
                "message": message
                
            })

        # comment submitted by post, added to comment table
        elif "comment" in request.POST:

            Comment.objects.create(
                auction=auction,
                user=request.user,
                content=request.POST.get("comment")      
            )
            return HttpResponseRedirect(reverse("listpage", args=(listpage,)))

        elif "status" in request.POST:
            # the button will submit empty string, thus will be none, hence status will be stored as Boolean Value - False
            auction.status = False
            auction.save()
            message = "Auction Closed"

            return render(request, "auctions/listpage.html", {
                "auction": auction,
                "watchlist_exist":  watchlist_exist,
                "comments": comment,
                "owner": owner,
                "auction_closed_alert":message
            })
            


@login_required
def create(request):
    if request.method =="GET":
        form = AuctionForm()
        return render(request, "auctions/create.html",{
            "form":form
        })
    else:
        form = AuctionForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.user = request.user
            auction.save()            
        return HttpResponseRedirect(reverse("index"))
    
@login_required
def watchlist(request):
    if request.method == "POST":
        # add the many to many relationship in the Auction & User join table
        auction = Auction.objects.get(pk=request.POST.get("auction")) 
        user = request.user
        auction.watcher.add(user)
        return render(request,"auctions/watchlist.html",{
             "auctions": request.user.watchlist.all()
        })
    else:
        return render(request, "auctions/watchlist.html",{
            "auctions": request.user.watchlist.all()
        })
    
@login_required
def mylisting(request):
    if request.method=="GET":
        mylisting = request.user.auctions.all()
        return render(request, "auctions/mylisting.html",{
            "mylistings": mylisting
        })

        #need to add a page for user to see all their listing and then can amend their listing

@login_required
def category(request):
    categories = Category.objects.all()
    return render(request, "auctions/category.html",{
        "categories" : categories
    })

@login_required
def amend(request, listingID):
    auction = Auction.objects.get(pk=listingID)
    form = AuctionForm(instance = auction)
    if request.method =="GET":
        return render(request, "auctions/amend.html",{
            "auction":auction,
            "form":form
        })
    else:
        form = AuctionForm(request.POST, instance=auction)

        if form.is_valid():
            auction = form.save()
            return HttpResponseRedirect(reverse("mylisting"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
