from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("createlisting", views.create_listing, name="createlisting"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("category/<str:category>", views.category, name="category"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
