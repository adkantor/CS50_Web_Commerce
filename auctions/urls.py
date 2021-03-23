from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.create_listing, name="create_listing"),
    path("listings/<int:listing_id>", views.show_listing, name="show_listing"),
    path("watch", views.add_to_watchlist, name="add_to_watchlist"),
    path("unwatch", views.remove_from_watchlist, name="remove_from_watchlist")
]
