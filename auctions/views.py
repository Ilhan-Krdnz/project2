from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .forms import AuctionForms, CommentForms, BidForms
from .models import User, Auctions, Comment, Watchlist

def index(request):
    display = Auctions.objects.all()
    return render(request, "auctions/index.html",context={
        'display': display,
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

def make_listing(request):
    formdata = AuctionForms(request.POST, request.FILES)
    if request.method == "POST":
        if formdata.is_valid():
            auction = formdata.save(commit=False)
            auction.user = request.user
            auction.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            formdata = AuctionForms()

    return render(request, "auctions/make_listing.html",context={
        'form':formdata
        })

def comment(request, pk):
    display = Auctions.objects.all()
    formdata = CommentForms(request.POST or None)
    formAuction = get_object_or_404(Auctions, pk=pk)
    if request.method == "POST":
        if formdata.is_valid():
            the_auction = formdata.save(commit=False)
            the_auction.user = request.user
            the_auction.auction = formAuction
            the_auction.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            formdata = CommentForms()

    return render(request, "auctions/comment.html",context={
    "display":display,
    "formdata":formdata,
    "auction":formAuction,
    })
'''def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return HttpResponseRedirect(reverse("index"))'''
def bidding(request, pk):
    formdata = BidForms(request.POST or None)
    formAuction = get_object_or_404(Auctions, pk=pk)
    if request.method == "POST":
        the_auction = formdata.save(commit=False)
        the_auction.user = request.user
        the_auction.auction = formAuction
        the_auction.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        formdata = BidForms()

    return render(request,"auctions/bidding.html",context={
        "formdata":formdata,
        'auction':formAuction,
        })

def add_watchlist(request, pk):
    the_auction = get_object_or_404(Auctions, pk=pk)
    if 'message' not in request.session:
        pass
    request.session['message'] = []
    
    for i in Watchlist.objects.all():
        watchlist_auction = i.auction.get()
        if the_auction.user == watchlist_auction.user and the_auction.pk == watchlist_auction.pk:
            #request.session['message'] = 'it is already in your watchlist' 
            return HttpResponseRedirect(reverse("watchlist"))
    else:
        message = None
        the_watchlist = Watchlist(user=request.user)
        the_watchlist.save()
        the_watchlist.auction.add(the_auction)
        return HttpResponseRedirect(reverse('watchlist'))
    
    return render(request, 'auctions/add_watchlist.html',context={
        'auction':the_auction
        })

def watchlist(request):
    display = Watchlist.objects.all()
    auction_list = []
    #message = request.session['message']
    # this for loop is a very important lesson
    for i in display:
        auction_list.append(i.auction.get())
    
    return render(request,'auctions/watchlist.html',context={
        'auction_list':auction_list,
        #'message': request.session['message'],
        })