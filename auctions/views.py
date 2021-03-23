from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing


class ListingForm(forms.ModelForm):
    """ Form to create a new listing. """
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']


def index(request):
    # get list of active listings
    listings = Listing.objects.filter(is_active=True)
    print(listings)
    return render(request, "auctions/index.html", {
        "listings": listings
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


def create_listing(request):
    if request.method == 'POST':
        # load the contents of the posted form into a variable
        form = ListingForm(request.POST)
        
        # validate by server
        if form.is_valid():
            listing = form.save(commit=False)
            listing.created_by = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            # return the filled-in form with error message
            return render(request, "auctions/createlisting.html", {
                "message": "Invalid form data",
                "form": form
            })
    
    else:
        return render(request, "auctions/createlisting.html", {
            "form": ListingForm()
        })


def show_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    # TODO: if listing then ... else ... -> esetleg hthml-ben, ha none
    return render(request, "auctions/showlisting.html", {
        "listing": listing
    })

def add_to_watchlist(request):
    listing_id = int(request.GET.get('listingId'))
    listing = Listing.objects.get(pk=listing_id)
    request.user.watchlisted_items.add(listing)
    print(f'Add to watchlist: \n{listing}')
    return render(request, "auctions/showlisting.html", {
        "listing": listing
    })

def remove_from_watchlist(request):
    listing_id = int(request.GET.get('listingId'))
    listing = Listing.objects.get(pk=listing_id)
    request.user.watchlisted_items.remove(listing)
    print(f'Remove from watchlist: \n{listing}')
    return render(request, "auctions/showlisting.html", {
        "listing": listing
    })