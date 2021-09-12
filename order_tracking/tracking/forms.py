from django.contrib.gis import forms
from .models import *
from mapwidgets.widgets import GooglePointFieldWidget, GoogleStaticOverlayMapWidget

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__" 
        # widgets = {
        #     'coordinates': GooglePointFieldWidget,
        #     'location': GoogleStaticOverlayMapWidget,
        # }  