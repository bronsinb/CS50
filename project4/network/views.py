import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post

def new_edit_post(request):
    post = request.POST["post"]
    if len(post) > 0:
        if request.POST["posttype"] == 'post':
            post = Post(user=request.user, text=post)
            post.save()
        else:
            oldpost = Post.objects.get(pk=int(request.POST["posttype"]))
            oldpost.text = post
            oldpost.save()

def index(request):
    if request.method == "POST":
        new_edit_post(request)

    posts = Post.objects.all().order_by('created').reverse()

    return render(request, "network/index.html", {
        "posts": posts,
        "name": "All Posts"
    })

def following(request):

    posts = Post.objects.all().filter(user__in=request.user.following.all())

    print(posts)
    
    return render(request, "network/index.html", {
        "posts": posts,
        "name": "Following"
    })

def profile(request, username):
    if request.method == "POST":
        new_edit_post(request)

    profile = User.objects.get(username=username)

    return render(request, "network/profile.html", {
        "posts": profile.posts.all(),
        "profile": profile,
        "following": request.user in profile.follower.all()
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def like(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
        return JsonResponse({"like": False, "amount": len(post.likes.all())}, status=200)
    else:
        post.likes.add(request.user)
        return JsonResponse({"like": True, "amount": len(post.likes.all())}, status=200)

@login_required
def follow(request, user_id):

    # Query for requested user
    try:
        profile = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    if request.user in profile.follower.all():
        profile.follower.remove(request.user)
        return JsonResponse({"follow": False, "amount": len(profile.follower.all())}, status=200)
    else:
        profile.follower.add(request.user)
        return JsonResponse({"follow": True, "amount": len(profile.follower.all())}, status=200)