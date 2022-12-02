import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, PostForm, Follow

def index(request):
    # Get user information
    user = User.objects.get(username=request.user)

    # Retrieve all posts in reverse chronological order
    posts = Post.objects.all().order_by('timestamp').reverse()

    # Add paginator
    paginator = Paginator(posts, 10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "user": user,
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

    # Add paginator
    paginator = Paginator(userposts, 10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    return render(request, "network/user.html", {
        "username": user.username,
        "page_obj": page_obj,
        "ownpage": ownPage,
        "isfollowing": isFollowing,
        "following": followingCount,
        "follower": followedCount
    })

@login_required(login_url='/login')
def following(request):
    # Access username of actual user i.e. watcher
    watcher = User.objects.get(username=request.user)
    
    # Get a list of users followed by watcher
    followall = watcher.following.all()
    following = [f.followed for f in followall]

    # Access all posts from following users
    followposts = Post.objects.filter(user__in=following).order_by('timestamp').reverse()

    
    # Add paginator
    paginator = Paginator(followposts, 10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    return render(request, "network/following.html", {
        "page_obj": page_obj,
    })

@csrf_exempt
@login_required(login_url="/login")
def edit(request, post_id):

    # Query for requested post
    try: 
        post = Post.objects.get(pk=post_id) 
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())
    
    # Update post if post is submitted
    elif request.method == "PUT":
        data = json.loads(request.body)
        post.content = data["content"]
        post.save()
        return HttpResponse(status=204)
    
    # Post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


@csrf_exempt
@login_required(login_url="/login")
def like(request, post_id):

    # Query for requested post
    try: 
        post = Post.objects.get(pk=post_id) 
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())
    
    # Update post if post is submitted
    elif request.method == "PUT":
        data = json.loads(request.body)
        user = User.objects.get(username=request.user)
        post.likes.add(user)
        post.save()
        return HttpResponse(status=204)
    
    # Post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)