from django.shortcuts import render
from rest_framework.serializers import Serializer
from .models import *
import requests
from .forms import *
from .serializers import *    
from rest_framework.generics import ListCreateAPIView,ListAPIView, RetrieveAPIView,RetrieveUpdateAPIView
from django.http import JsonResponse
from rest_framework.response import Response
from django.contrib.gis.geos import Point

# Create your views here.

from geopy.geocoders import Nominatim
import json
geolocator = Nominatim(user_agent="tracking")
api="d611419749b667a306600e1772193619"

class Orders(ListAPIView):
    queryset=Order.objects.all()             
    serializer_class=PlaceSerializer 
    
class OrderDetails(RetrieveAPIView):             
    queryset=Order.objects.all()                    
    serializer_class=PlaceSerializer    
    lookup_field="id" 
    
class OrderCreate(ListCreateAPIView):             
    queryset=Order.objects.all()                 
    serializer_class=PlaceSerializer        

    def perform_create(self,serializer): 
        lat_lng= serializer.initial_data["lat_lng"]  
        query=serializer.initial_data["address"]  
        if lat_lng:
            url_2=requests.get(f"http://api.positionstack.com/v1/reverse?access_key={api}&query={lat_lng}")
            results=url_2.json()
        elif query:
            url=requests.get(f"http://api.positionstack.com/v1/forward?access_key={api}&query={query}")
            results=url.json() 
            print(results)
        try:   
            filters={}
            for i in results["data"]:
                if i["country"] == "Egypt": 
                    filters["country"] = i["country"]
                    filters["region"]= i["region"]          
                    filters["lattitude"] = i["latitude"]
                    filters["longitude"]=i["longitude"]
            filters=json.dumps(filters,indent = 4)
            my_json=json.loads(filters) 
            print(my_json)       
            if serializer.is_valid():       
               
                lat=my_json["lattitude"]    
                lng=my_json["longitude"]   
               
                serializer.save(user=self.request.user,lat_lng=f"{lat},{lng}")
                message={"message":my_json}   
                return Response(message) 
        
        except: 
            message={"message":"sorry there is an issue finding you location"}   
            return Response(message) 


class OrderConfirm(ListCreateAPIView):
    serializer_class=OrderSerializer
    queryset=Driver.objects.all()
    def post(self,request):
        serializer=OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            order=Order.objects.get(id=serializer.initial_data["order"])
            order.ordered=True    
            order.save()
           
        return Response(serializer.data)
    
class OrderUpdate(RetrieveUpdateAPIView):
    serializer_class=OrderUpdateSerializer
    queryset=Driver.objects.filter(order__ordered=True)
    lookup_field="id" 
    def peroform_create(self,serializer):
        if serializer.is_valid():
            serializer.save()   
            # message={"message":serializer}      
        return Response(serializer.data)
        

   