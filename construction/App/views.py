from django.shortcuts import render,redirect,reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user,logout as logout_user
# Create your views here.


def home(request):
    return render(request,"index.html")
def products(request):
    return render(request,"products.html")
def about(request):
    return render(request,"about.html")
def bill(request):
    return render(request,"bill.html")
def register_users(request):
    if request.user.is_authenticated:
        return redirect(reverse("home:home")) 
    if request.method == 'POST':
        username=request.POST.get("login")
        password=request.POST.get("password")    
        for i in User.objects.all():    
            if username in  i.username:
                messages.error(request,"invalid username")
                return redirect(reverse("home:register"))
            else:     
                User.objects.create_user(username=username,password=password)
                new_user=authenticate(username=username,password=password)
                login_user(request,new_user)      
                messages.success(request,f"{username} registered successflly")
                return redirect(reverse("home:home"))
    return render(request,"signup.html")      
def login(request): 
    if request.user.is_authenticated:
        return redirect(reverse("home:home"))  
    if request.method == 'POST':
        username=request.POST.get("login")
        password=request.POST.get("password")
        user=authenticate(username=username,password=password)
        if user is not None:
            login_user(request,user)
            messages.success(request,f"logged in as {username}")
            return redirect(reverse("home:home"))
        else:
            messages.error(request,"invalid account")
    return render(request,"signin.html")
    
def logout(request):
    if request.user.is_anonymous:
        return redirect(reverse("home:home"))
    logout_user(request)
    return redirect(reverse("home:home"))          




