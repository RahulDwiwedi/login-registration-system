# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from forms import RegistrationForm
from django.template import RequestContext
from forms import UserProfileForm

# Create your views here.

def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile')
    c={}
    c.update(csrf(request))
    return render(request, 'login.html',c)

def auth_view(request):
    username=request.POST.get('uname',"")
    password=request.POST.get('psw',"")
    user = auth.authenticate(username=username,password=password)

    if user is not None:
        auth.login(request,user)
        print request.user.username
        return HttpResponseRedirect('/profile')
    else:
        msg="Wrong Username or Password ....Please Try again."
        return render(request, 'login.html',{'msg': msg}) 

@login_required(login_url='/')
def profile(request):
    return render(request, 'profile.html')

def logout(request):
    auth.logout(request)
    msg="Sucessfully Logout....Please Login Again"
    return render(request, 'login.html',{"msg":msg})
    
def user_registration(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile')
    args={}
    args.update(csrf(request))
    if request.method=="POST":
        form1=RegistrationForm(request.POST)
        form2=UserProfileForm(request.POST)
        args["err"] = form1.errors
        args["err2"]= form2.errors
        if form1.is_valid() * form2.is_valid():
            user=form1.save()
            userprofile=form2.save(commit=False)
            userprofile.user=user
            userprofile.save()
            return HttpResponseRedirect('/register_success')
    

    args["form"] = RegistrationForm()
    args["form2"] = UserProfileForm()
    return render(request, 'register.html',args, RequestContext(request))

    

def register_success(request):
    msg="Register Successful ...Please Login"
    return render(request, 'login.html',{'msg': msg})





    
