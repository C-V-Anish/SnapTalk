from django.shortcuts import render,redirect
from dotenv import load_dotenv
from .forms import RegisterForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import os
# Create your views here.

load_dotenv(".env")
APP_ID = os.environ.get("ZEGO_CLOUD_APP_ID")
SERVER_SECRET = os.environ.get("ZEGO_CLOUD_APP_SERVER_SECRET")


def register_user(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            print("Success")
            return render(request,"login.html",{'success':'Registration Successful. Please Log In.'})
        else:
            error_message=form.errors.as_text()
            print(error_message)
            return render(request,"register.html",{'error':error_message})
    
    return render(request,"register.html")
        
def login_user(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(request,username=email,password=password)
        if user is not None:
            login(request,user)
            return redirect("/dashboard")
        else:
            return render(request,"login.html",{"error":"Invalid Credentials. Please try again."})
        
    return render(request,"login.html")

@login_required
def dashboard_user(request):
    return render(request,"dashboard.html",{"name":request.user.first_name})

@login_required
def videocall(request):
    return render(request,"videocall.html",{"name":request.user.first_name + " " + request.user.last_name, "APP_ID":APP_ID, "SERVER_SECRET":SERVER_SECRET})

@login_required
def logout_user(request):
    logout(request)
    return redirect("/login")

@login_required
def join_room(request):
    if request.method=='POST':
        roomId=request.POST.get("roomId")
        return redirect("/meeting/?roomID="+roomId)
    return render(request,"joinroom.html")