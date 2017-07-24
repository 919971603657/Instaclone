# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect


from forms import SignUpForm, LoginForm,PostForm
from datetime import datetime
from models import UserModel, SessionToken,PostModel
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from instaclone.settings import BASE_DIR
from imgurpython import ImgurClient

# Create your views here.

def signup_view(request):
   if request.method == "POST":
       form = SignUpForm(request.POST)
       print request.body
       if form.is_valid():
           print "ABCD"
           username = form.cleaned_data['username']
           name = form.cleaned_data['name']
           email = form.cleaned_data['email']
           password = form.cleaned_data['password']
           user = UserModel(name=name, password=make_password(password), email=email, username=username)
           user.save()
       return render(request, 'success.html')
   elif request.method == "GET":
       form = SignUpForm()
       today = datetime.now()


   return render(request, 'index.html', { 'today': today,  'form': form})



def login_view(request):
    response_data = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            print "here"
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print UserModel.objects.all()
            user = UserModel.objects.filter(username=username).first()
            print user

            if user:
                # Check for the password
                print 'A'
                if check_password(password, user.password):
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    response_data['message'] = 'Incorrect Password! Please try again!'

    elif request.method == 'GET':
        form = LoginForm()

    response_data['form']= form
    return render(request, 'login.html', response_data)

def feed_view(request):
    return render(request, 'feed.html')




def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            return session.user
    else:
        return None


def post_view(request):
    user = check_validation(request)

    if user:
        if request.method == 'POST':

          form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get('image')
            caption = form.cleaned_data.get('caption')
            post = PostModel(user=user,image=image,caption=caption)
            post.save()
            path = str(BASE_DIR + "/" + post.image.url)
            client = ImgurClient('8fd0103958ccceb', 'aa73c860636e25e381ec473bd76fb4f2d3ca1adb')
            post.image_url = client.upload_from_path(path, anon=True)['link']
            post.save()
            return redirect('/feed/')
        else:
          form = PostForm()
        return render(request, 'post.html', {'form': form})
    else:
        return redirect('/login/')

def feed_view(request):
    user = check_validation(request)
    if user:

        posts = PostModel.objects.all().order_by('created_on')

        return render(request, 'feed.html', {'posts': posts})
    else:

        return redirect('/login/')


def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            return session.user
    else:
            return None






