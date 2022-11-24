import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, PostForm, Follow

def index(request):
    posts = Post.objects.all().order_by('timestamp').reverse()
    return render(request, "network/index.html", {
        "posts": posts,
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

def compose(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = user
            post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/compose.html", {
            "form": PostForm()
        })

def user(request, username):
    # Access username of actual user
    watcher = User.objects.get(username=request.user)

    # Access username of requested page
    user = User.objects.get(username=username)

    # Access all their posts
    posts = Post.objects.all()
    userposts = posts.filter(user=user.id).order_by('timestamp').reverse()

    # See following/follower count
    following = Follow.objects.all().filter(user=user.id).count()
    followed = user.follower.all().count()

    if user == watcher:
        return render(request, "network/user.html", {
            "username": user.username,
            "posts": userposts,
            "ownpage": True,
            "following": following,
            "followed": followed
        })
    else:
        return render(request, "network/user.html", {
            "username": user.username,
            "posts": userposts,
            "ownpage": False,
            "following": following,
            "followed": followed
        })

    