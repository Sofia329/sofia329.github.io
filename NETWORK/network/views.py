import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post

def index(request):
    # Authenticated users view posts
    if request.user.is_authenticated:
        return render(request, "network/index.html")
    else:
        return HttpResponseRedirect(reverse("login"))
    
@login_required
@csrf_exempt
def newpost(request):
    if request.method!="POST":
        return JsonResponse({"error": "POST request required"}, status = 400)
    
    # check if post is empty
    data = json.loads(request.body)
    content = data.get("content") 
    if not content:
        return JsonResponse({
            "error": "Post cannot be empty"
        }, status = 400)
    
    #save new post into database
    post = Post(
        poster = request.user,
        content = content
    )
    post.save()
    return JsonResponse({"message": "Posted Successfully."}, status=201)


def allposts(request):
    # get request to get all posts in chronological orders
    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return JsonResponse({
        "posts":[post.serialize() for post in page_obj],
        "has_next":page_obj.has_next(),
        "has_previous": page_obj.has_previous()
    })

@login_required
@csrf_exempt
def editpost(request, post_id):
    if request.method == "GET":
        try:
            # only the current user == poster of the Post, will be able to edit the post
            post = Post.objects.get(id=post_id, poster = request.user)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post is not found."}, status = 404)
        return JsonResponse(post.serialize())
    
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            try:
                 # only the current user == poster of the Post, will be able to edit the post
                post = Post.objects.get(id=post_id, poster = request.user)
            except Post.DoesNotExist:
                return JsonResponse({"error": "Post is not found."}, status = 404)
            post.content = data.get("content")
            post.save()
            return JsonResponse({"message": "Edit Post Successfully", 
                                 "post": post.serialize()}, status = 200)
    
        if data.get("likes") is not None:
            try:
                # anyone can like the post
                post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                return JsonResponse({"error": "Post is not found."}, status = 404)
            if data.get("likes") > post.likes:
                post.likes = data.get("likes")
                post.save()
                return JsonResponse({"message": "Liked Post Successfully", 
                                        "post": post.serialize()}, status = 200)
            else: 
                post.likes = data.get("likes")
                post.save()
                return JsonResponse({"message": "Unliked Post Successfully", 
                                        "post": post.serialize()}, status = 200)
    else: 
        return JsonResponse({"error": "GET or PUT request required."}, status=400)


@login_required
@csrf_exempt
def profile(request, username):
    # query for requested user_id profile 
    try: 
        currentuser = request.user.username
        user = User.objects.get(username=username)
        followers = user.followers.count()
        following = user.following.count()
        posts = user.posts.all().order_by("-timestamp")
        is_following = user.followers.filter(id = request.user.id).exists()

        #Pagination on Posts
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except User.DoesNotExist:
        return JsonResponse({"error": "User Profile not found."}, status = 404)

    # return user profile
    if request.method == "GET":
        return JsonResponse({
            "currentuser": currentuser,
            "username": username,
            "followers": followers,
            "following":following,
            "is_following": is_following,
            "posts": [post.serialize() for post in page_obj],
            "has_next": page_obj.has_next(),
            "has_previous":page_obj.has_previous()
        })
    
    # add/remove followers via PUT
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("is_following") is not None:
            if data.get("is_following"):
                request.user.following.add(user)
                return JsonResponse({"message": "Followed Successfully", "followers": user.followers.count()}, status=200)
            else:
                request.user.following.remove(user)
                return JsonResponse({"message": "Unfollowed Successfully", "followers": user.followers.count()}, status=200)
            
    # Profile must be via Get or Put  
    else: return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)
            
@login_required
def myposts(request):
    myposts = request.user.posts.all().order_by("-timestamp")
    #Pagination: display 10 on a page
    paginator = Paginator(myposts,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/myposts.html",{
        "myposts": page_obj
    })

@login_required
def following(request):
    # all the current user's following
    following =  request.user.following.all()
    posts = []
    for user in following: 
        for post in user.posts.all():
            posts.append(post)

    # sort in reverse chronological order
    posts.sort(key = lambda post: post.timestamp , reverse=True)

    # Pagination: display 10 on a page
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render (request, "network/following.html",{
        "following": following,
        "posts": page_obj })
    

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
