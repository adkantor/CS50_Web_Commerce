from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    """ Class to represent a listing. """
    CATEGORIES = [
        ("fashion", "Fashion"),
        ("toys", "Toys"),
        ("electronics", "Electronics"),
        ("home", "Home"),
        ("other", "Other")
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=100, choices=CATEGORIES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings', null=True)
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True)
    watchlisted_by = models.ManyToManyField(User, blank=True, related_name='watchlisted_items')


class Bid(models.Model):
    pass


class Comment(models.Model):
    pass 

