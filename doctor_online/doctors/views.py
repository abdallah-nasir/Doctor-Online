from django.shortcuts import (get_object_or_404, render,redirect,reverse)
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.decorators import login_required
get_object_or_404
from django.contrib import messages
# Create your views here.

def home(request):  
    if request.user.is_authenticated and request.user.profile.type == "doctor":
        clinics=Clinic.objects.filter(doctor__user=request.user)
        reseravtions=None
    else: 
        try:
            reseravtions=Reservation.objects.filter(patient=request.user)
        except:
            reseravtions=[]  
        clinics=Clinic.objects.all()
    context={"clinics":clinics,"reseravtions":reseravtions}
    return render(request,"home.html",context)   
def signin(request):
    if request.user.is_authenticated:
        messages.error(request,"you are alreadylogedin")
        return redirect(reverse('home:home'))
    if request.method == "POST":
        
        username=request.POST.get("username")
        password=request.POST.get("password")
        username=authenticate(request,username=username,password=password)
        if username is not None:
            login(request, username)
            messages.success(request,f"signed in as {username}")
            return redirect(reverse("home:home"))
        else:
            messages.error(request,"invalid username/password")
    return render(request,"signin.html")  

def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse("home:home"))
    form=None
    if request.method == "POST":
        username =request.POST.get('username')
        last_name=request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        type=request.POST.get("type")
        form=UserCreationForm(request.POST)
        try:
            if form.is_valid():
                if type == "doctor" or type == "patient":
                    instance=form.save(commit=False)
                    instance.first_name=username    
                    instance.last_name=last_name
                    instance.email=email
                    instance.save()
                    Profile.objects.create(user=instance,type=type)
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    return redirect(reverse('home:home'))
                else:
                    messages.error(request,"invalid data")

            else:
                messages.error(request,f"{form.errors}")
        except:   
            messages.error(request,"invalid data")
    context={"form":form}
    return render(request,"signup.html",context)
  
def signout(request):  
    if request.user.is_authenticated: 
        logout(request)
    else:
        messages.error(request,"you are already signed out")
    return redirect(reverse('home:home'))
@login_required(login_url="home:login")
def clinics_add(request): 
    profile=get_object_or_404(Profile,user=request.user,type="doctor")
    # clinic=get_object_or_404(Clinic,id=id,doctor=profile)
    if request.method == 'POST':       
        name=request.POST.get("name")  
        price=request.POST.get("price")
        days=request.POST.getlist("days")
        start_time=request.POST.get("start_time")
        end_time=request.POST.get("end_time")
       
        try:  
            clinic=Clinic.objects.create(doctor=profile,name=name,price=price,days=days,start_time=start_time,end_time=end_time)
            messages.success(request,"clinic added successfully")
            return redirect(reverse("home:home"))
        except:   
            messages.error(request,"invalid data")  
    context={}
    return render(request,"clinic_add.html",context)

@login_required(login_url="home:login")
def clinics_edit(request,id): 
    profile=get_object_or_404(Profile,user=request.user,type="doctor")
    clinic=get_object_or_404(Clinic,id=id,doctor=profile)
    if request.method == 'POST':       
        name=request.POST.get("name")  
        price=request.POST.get("price")
        days=request.POST.getlist("days")
        start_time=request.POST.get("start_time")
        end_time=request.POST.get("end_time")
        try:  
            clinic.name=name
            clinic.price=price
            clinic.days=days
            clinic.start_time=start_time
            clinic.end_time=end_time
            clinic.save()
            messages.success(request,"clinic added successfully")
            return redirect(reverse("home:home"))
        except:   
            messages.error(request,"invalid data")  
    context={"clinic":clinic}
    return render(request,"clinic_edit.html",context)
def clinic_delete(request,id):
    clinic=get_object_or_404(Clinic,doctor=request.user.profile,id=id)
    clinic.delete()
    return redirect(reverse("home:home"))
from datetime import datetime
@login_required(login_url="home:login")
def resereve(request,id):
    profile=Profile.objects.get(user=request.user)
    if profile.type == 'doctor':
        messages.error(request,"you cant reserve as a Doctor account")
        return redirect(reverse("home:home"))
    else:
        clinic=Clinic.objects.get(id=id)
        if Reservation.objects.filter(patient=request.user,clinic=clinic).exists():
            messages.error(request,"you are already have an appointment ")
            return redirect(reverse("home:home"))

        if request.method == 'POST':
            days=request.POST.getlist("days")
            time=request.POST.get("time")           
            if days == []:  
                messages.error(request,'you must,choose a day')
                return redirect(reverse("home:reserve",kwargs={"id":clinic.id}))
  
            for i in days:     
                if i not in clinic.days:
                    messages.error(request,'sorry,clinic is not open on this day/s')
                    return redirect(reverse("home:reserve",kwargs={"id":clinic.id}))

            Reservation.objects.create(doctor=clinic.doctor,time=time,clinic=clinic,patient=request.user)
            messages.success(request,"your Reservation has been submitted successfully")
            return redirect(reverse("home:home"))  

    context={"clinic":clinic}      
    return render(request,"reserve.html",context)

@login_required(login_url="home:login")
def reserve_delete(request,id):
    clinic=Clinic.objects.get(id=id)
    reserve=Reservation.objects.get(patient=request.user,clinic=clinic)
    reserve.delete()
    return redirect(reverse("home:home"))  

def type(request):
    if request.user.is_authenticated:
        try:
            profile=Profile.objects.get(user=request.user)
            if profile.type == "doctor":
                doctor=True
            else:
                doctor=False
        except:
            doctor=False
    else:  
        doctor=False
    context={"doctor":doctor}
    return context
           
           
