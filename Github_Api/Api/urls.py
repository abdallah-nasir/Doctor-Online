from django.urls import path
from . import views
from .views import *

app_name="Api"
urlpatterns = [
# path("",github.as_view(),name="github"),
path("",views.github,name="github")

]

 