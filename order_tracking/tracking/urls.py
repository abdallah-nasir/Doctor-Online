from django.urls import path
from . import views
from .views import *
app_name="tracking"

urlpatterns = [  
path("",Orders.as_view(),name="home"),
path("create/",OrderCreate.as_view(),name="create"),
path("details/<str:id>/",OrderDetails.as_view(),name="details"),
path("order/confirm/",OrderConfirm.as_view(),name="confirm"),
path("order/update/<str:id>/",OrderUpdate.as_view(),name="update"),

]
                  
                  
                  