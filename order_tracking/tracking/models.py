from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from location_field.models.spatial import LocationField
from location_field.models.plain import PlainLocationField
from django.contrib.auth.models import User
# Create your models here.
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=255) #optinal
    lat_lng = PlainLocationField(blank=True,null=True,zoom=7)
    ordered=models.BooleanField(default=False)
        
    def __str__(self):
        return self.user.username
    
    
class Driver(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    # my_address=models.CharField(max_length=255) 
    my_location=PlainLocationField(zoom=7) #(lat,lng) only
    def __str__(self):
        return str(self.order.id)