from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
# from social.settings import MEDIA_ROOT

from .models import User, Post, Profile, Comment
from .forms import ProfileEditForm, PostForm, UserEditForm, ChangePasswordForm, LoginForm
import os



@login_required(login_url='login')
def index(request):
    message = None
    if request.method == 'POST':
        if request.POST.get('comment', False):
            post = Post.objects.get(id=request.POST['id'])
            comment = Comment.objects.create(post=post, content=request.POST['comment'], commenter=request.user)
            comment.save()
        if request.POST.get('post-content', False):
            post = Post.objects.create(content=request.POST['post-content'], creator=request.user)
            post.save()
            messages.success(request, 'Created New Post')
    posts = Post.objects.all()
    comments = [[comment for comment in post.comments.all()] for post in posts][::-1]
    commenterCount = ([len(set([comment.commenter for comment in post.comments.all() ])) for post in posts])[::-1]
    return render(request, "network/home.html", {
        'posts' : zip(posts[::-1],commenterCount, comments),
    })

def loginView(request):
    message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            message = 'Enter a Valid Username and Password'

    return render(request, "network/login.html", {
        "message" : message
    })

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        confirmation = request.POST['password2']
        if confirmation !=password:
            return HttpResponseRedirect(reverse('register'), {"message" : "Passwords Doesn't Match"})
        try:
            user= User.objects.create_user(username=username, email=email, password=password)
        except IntegrityError:
            return HttpResponseRedirect(reverse('register'), {"message" : "User Already Exist. Try Login In"})
        login(request, user)
        return HttpResponseRedirect(reverse('home'), {"message": "You've Logged In"}) 
    return render(request, "network/register.html")


def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url='login')
def profileView(request, id):

    userForm = UserEditForm(instance=request.user)
    profileForm = ProfileEditForm(instance=request.user.profile)

    if request.method == 'POST':
        userForm = UserEditForm(request.POST, instance=request.user)
        profileForm = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()

    user = User.objects.get(id=id)
    userPosts = Post.objects.filter(creator=user)
    followAction = 'unfollow' if user in request.user.profile.following.all() else 'follow'
    comments = [[comment for comment in post.comments.all()] for post in userPosts][::-1]
    commenterCount = ([len(set([comment.commenter for comment in post.comments.all() ])) for post in userPosts])[::-1]
    return render(request, 'network/profile.html', {
        'profile' : user.profile,
        'posts' : zip(userPosts[::-1], commenterCount, comments),
        'follow' : followAction,
        'userForm' : userForm,
        'profileForm' : profileForm
    })

@login_required(login_url='login')
def followingView(request):
    followings = request.user.profile.following.all()
    followingPosts = [post for following in followings for post in following.posts.all()]
    comments = [[comment for comment in post.comments.all()] for post in followingPosts][::-1]
    commenterCount = ([len(set([comment.commenter for comment in post.comments.all() ])) for post in followingPosts])[::-1]
    return render(request, 'network/following.html', {
        'posts': zip(followingPosts[::-1], commenterCount, comments)
    })

def likePostView(request, id):
    post = Post.objects.get(id=id)
    if request.user in post.likedUsers.all():
       post.likedUsers.remove(request.user)
    else:
       post.likedUsers.add(request.user)
    return JsonResponse({
        'numLikes' : f'{post.likedUsers.count()}'
    })

@login_required(login_url='login')
def deletePost(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    messages.success(request, 'Post Removed')
    return redirect('home')

@login_required(login_url='login')
def editPost(request, id):
    post = Post.objects.get(id=id)
    form = PostForm(request.POST, instance=post)
    
    if form.is_valid():
        form.save()
        messages.success(request, 'Post Edited')
    return redirect('home')

@login_required(login_url='login')
def follow(request, id):
    status = 'unfollow'
    user = Profile.objects.get(id=id).user
    profile = request.user.profile
    if user in profile.following.all():
        profile.following.remove(user)
        status = 'follow'
    else: 
        profile.following.add(user)
    return JsonResponse({
        'status' : status
    })

@login_required(login_url='login')
def passwordReset(request, id):
    form = ChangePasswordForm(request.user)
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Password has been Changed')
            update_session_auth_hash(request, form.user)
    return render(request, 'network/passwordReset.html', {
        'form' : form,
        'profile' : Profile.objects.get(id=id)
    })

def likeCommentView(request, id):
    comment = Comment.objects.get(id=id)
    if request.user in comment.likedUsers.all():
       comment.likedUsers.remove(request.user)
    else:
       comment.likedUsers.add(request.user)
    return JsonResponse({
        'numLikes' : f'{comment.likedUsers.count()}'
    })