from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.forms.widgets import NumberInput
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.db.models import Max

from .models import User, Listing, Bid


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
        next = request.POST["next"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if next:
                return HttpResponseRedirect(next)
            else:
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
    """ Records a new listing to the database """
    
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
    """ Shows a page specific to the listing given as parameter. """

    # get listing
    listing = Listing.objects.get(pk=listing_id)
    current_bid = get_current_bid(listing)
    print(listing)
    print(current_bid)
    # show the page
    return render(request, "auctions/showlisting.html", {
        "listing": listing,
        "current_bid": get_current_bid(listing),
    })


@login_required(login_url='login')
def add_to_watchlist(request):
    """ Adds the listing to the user's watchlist. """
    
    # get listing
    listing_id = int(request.POST.get('listingId'))
    listing = Listing.objects.get(pk=listing_id)
    # add to user's watchlist
    request.user.watchlisted_items.add(listing)
    
    # return to the page
    return render(request, "auctions/showlisting.html", {
        "listing": listing,
        "current_bid": get_current_bid(listing),
    })


@login_required(login_url='login')
def remove_from_watchlist(request):
    """ Removes the listing from the user's watchlist. """

    # get listing
    listing_id = int(request.POST.get('listingId'))
    listing = Listing.objects.get(pk=listing_id)
    # remove from user's watchlist
    request.user.watchlisted_items.remove(listing)
    
    # return to the page
    return render(request, "auctions/showlisting.html", {
        "listing": listing,
        "current_bid": get_current_bid(listing),
    })

@login_required(login_url='login')
def make_bid(request):
    """ Records a new bid to the database. """
    
    # get listing
    listing_id = int(request.POST.get('listingId'))
    listing = Listing.objects.get(pk=listing_id)
    # get bid price
    bid_price = float(request.POST.get('bidPrice'))
    
    # check if bid price > current bid
    if bid_price > get_current_bid(listing).price:
       
        # create the new bid
        bid = Bid(
            bidder=request.user, 
            listing=listing,
            price=bid_price
        )
        bid.save()
        
        # return to the page
        return render(request, "auctions/showlisting.html", {
            "listing": listing,
            "current_bid": get_current_bid(listing),
        })
    
    else:
        
        # show error message
        return render(request, "auctions/showlisting.html", {
            "message": "Invalid bid (new bid price must be higher than current bid)",
            "listing": listing,
            "current_bid": get_current_bid(listing),
        })


def get_current_bid(listing):
    """ Helper function to get current bid from database. """
    current_bid = None
    max_bid_price = listing.bids.aggregate(max_bid=Max('price'))['max_bid']
    if max_bid_price:
        current_bid = Bid.objects.get(listing=listing, price=max_bid_price)
    return current_bid
