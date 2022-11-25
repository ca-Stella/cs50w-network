import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, PostForm, Follow

def index(request):
    # Retrieve all posts in reverse chronological order
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
    # If posting, then redirect to index after saving post
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
    followingCount = user.following.all().count()
    followedCount = user.followed.all().count()
    followLink = Follow.objects.filter(following = watcher, followed = user)

    # Initialize values for rendering
    ownPage = False
    isFollowing = False  

    # If request method is POST
    if request.method == "POST":
        # If follow or unfollow button is pressed
        if 'follow' or 'unfollow' in request.POST:
            # If follower, un-follow
            if followLink.exists():
                followLink.delete()
            # Else, add to following list
            else:
                watcherFollow = Follow()
                watcherFollow.following = watcher
                watcherFollow.followed = user
                watcherFollow.save()
        return HttpResponseRedirect(reverse("user", kwargs={
            "username": username,
        }))
    
    # If user is watcher, then label as so
    if user == watcher:
        ownPage = True
    
    # Else if follower is checking, label as so
    elif followLink.exists():
        isFollowing = True

    return render(request, "network/user.html", {
        "username": user.username,
        "posts": userposts,
        "ownpage": ownPage,
        "isfollowing": isFollowing,
        "following": followingCount,
        "follower": followedCount
    })