from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max


class User(AbstractUser):
    pass


class Listing(models.Model):
    """ Class to represent a listing. """
    
    def current_bid(self):
        """ Helper function to get highest bid for this listing. """
        bid = None
        max_bid_price = self.bids.aggregate(max_bid=Max('price'))['max_bid']
        if max_bid_price:
            bid = Bid.objects.get(listing=self, price=max_bid_price)
        return bid
    
    CATEGORIES = [
        ("fashion", "Fashion"),
        ("toys", "Toys"),
        ("electronics", "Electronics"),
        ("home", "Home"),
        ("other", "Other")
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=100, choices=CATEGORIES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings', null=True)
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True)
    watchlisted_by = models.ManyToManyField(User, blank=True, related_name='watchlisted_items')


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids', null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids', null=True)
    time = models.DateTimeField(auto_now_add=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)


class Comment(models.Model):
    pass 

