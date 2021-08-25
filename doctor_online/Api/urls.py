
from django.urls import path
from . import views
from .views import *

app_name="Api"

urlpatterns = [
    path('', views.ClinicList.as_view(),name="home"),
     path('clinic/<str:id>/', ClinicDetail.as_view(),name="details"),
      path('reservations/', ReservationsList.as_view(),name="reservations"),
     path('reserve/<str:id>/', Reservations_deatils.as_view(),name="reserve_details"),


]               