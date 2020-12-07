from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .forms import AuctionForms, CommentForms
from .models import User, Auctions, Comment

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
            formdata.save(commit=False)
            formdata.user = request.user
            formdata.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            formdata = AuctionForms()

    return render(request, "auctions/make_listing.html",context={
        'form':formdata
        })

def comment(request, pk):
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
    "formdata":formdata,
    "auction":formAuction,
    })