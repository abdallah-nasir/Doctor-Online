from django.urls import path
from . import views
from .views import *

app_name="App"

urlpatterns = [
path("",views.home,name="home"),
path("products/",views.products,name="products"),
path("about/",views.about,name="about"),
path("login/",views.login,name="login"),
path("register/",views.register_users,name="register"),
path("logout/",views.logout,name="logout"),


]
