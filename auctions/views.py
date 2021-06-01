from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Comment, Auction, Bid, Authors, Watchlist, Categories


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Auction.objects.all()
    })


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

def create(request):
    if request.method == "POST":
        title = request.POST["Title"]
        description = request.POST["description"]
        bid = request.POST["bid"]
        image = request.POST["image"]
        category = request.POST["category"]
        category = Categories.objects.get(category=category)
        auction = Auction(title=title,description=description,price=bid,image_url=image,category=category)
        authors = Authors(author=request.user, auction=auction)
        auction.save()
        authors.save()

        return HttpResponseRedirect(reverse("listing", args=[auction.id]))
    return render(request, "auctions/create.html", {
    })

def listing(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    author = Authors.objects.filter(auction=auction).first().author
    comments = Comment.objects.filter(auction=auction)
    array=[]
    for comment in comments:
        array+=[comment]
    addedMessage=""
    bidMessage=""
    msgColor="Red"
    if request.method == "POST": 
        if request.POST.get("add"):
            if not Watchlist.objects.filter(user=request.user,auction=auction):
                watchlist = Watchlist(user = request.user, auction = auction)
                watchlist.save()
                return HttpResponseRedirect(reverse("watchlist"))
            else:
                addedMessage="Item already added to watchlist!"
        elif request.POST.get("bid"):
            bidAmount = int(request.POST.get("bid"))
            if bidAmount>auction.price:
                if request.user != author:
                    bid = Bid(bid_price=bidAmount,auction=auction,user=request.user)
                    bid.save()
                    auction.price=bid
                    auction.save()
                    bidMessage="Successful bid!"
                    msgColor="Green"
                else:
                    bidMessage="Can't bid on your own listing!"
            else:
                bidMessage="You must place a bid higher than the current bid!"
        elif request.POST.get("close"):
            auction.delete()
            return HttpResponseRedirect(reverse("index"))
        elif request.POST.get("comment"):
            comment = Comment(text=request.POST.get("comment"),user=request.user,auction=auction)
            comment.save()
            return HttpResponseRedirect(reverse("listing", args=[auction.id]))

    return render(request, "auctions/listing.html", {
        "auction": auction,
        "author": author,
        "alreadyAdded": addedMessage,
        "bidMessage": bidMessage,
        "bidder": request.user,
        "msgColor":msgColor,
        "comments": array
    })

def watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user)
    array = []
    for item in watchlist:
        array+=[item]
    return render(request, "auctions/watchlist.html", {
        "watchlist": array
    })

def categories(request):
    categories = Categories.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def categoryAuction(request, category_category):
    category = Categories.objects.get(category=category_category)
    auction = Auction.objects.filter(category = category)
    return render(request, "auctions/categoryAuction.html", {
        "auctions": auction,
        "category": category
    })