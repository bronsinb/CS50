
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("like/<int:post_id>", views.like, name="like"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("edit/<int:post_id>", views.edit, name="edit"),
]
