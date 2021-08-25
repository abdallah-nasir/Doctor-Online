
from django.urls import path
from . import views
from .views import *

app_name="doctors"

urlpatterns = [
    path('', views.home,name="home"),
    path('login/', views.signin,name="login"),
    path('signup/', views.signup,name="signup"),
    path('signout/', views.signout,name="signout"),
    path('clinic/add/', views.clinics_add,name="clinic_add"),
    path('clinic/edit/<str:id>/', views.clinics_edit,name="clinic_edit"),
    path('clinic/delete/<str:id>/', views.clinic_delete,name="clinic_delete"),
    path('clinic/reserse/<str:id>/', views.resereve,name="reserve"),   
    path('clinic/reserse/delete/<str:id>/', views.reserve_delete,name="reserve_delete"),


]              