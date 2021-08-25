from django.shortcuts import render
from rest_framework.generics import (
	ListAPIView,
	RetrieveAPIView,
	UpdateAPIView,
	DestroyAPIView,
	CreateAPIView,
	RetrieveUpdateAPIView,
	RetrieveUpdateDestroyAPIView,
	ListCreateAPIView

)
from rest_framework.reverse import reverse
from .models import *
from .serializers import *
from .permissions import *   
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
# Create your views here.
          
 
class ClinicList(ListCreateAPIView):
    serializer_class=CliniDetailcSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
     
    def get_queryset(self):   
        qs=Clinic.objects.all().order_by('-id')
        return qs
            
    def post(self,request,format=None):
        if request.user.is_authenticated and request.user.profile.type == 'doctor':
            serializer = CliniDetailcSerializer(data=request.data)
            if serializer.is_valid():     
                Clinic.objects.create(doctor=request.user.profile,name=serializer.data["name"],price=serializer.data["price"],days=serializer.data["days"],start_time=serializer.data["start_time"],end_time=serializer.data["end_time"])
                context={"data":serializer.data,"message":"clinic added successffullt"}
                return Response(serializer.data)
            else:  
                return Response({"message": "invalid data"})    
        else:
            return Response({"message": "your are not a doctor"})  
class ClinicDetail(RetrieveUpdateDestroyAPIView):
    queryset=Clinic.objects.all()
    lookup_field="id"        
    serializer_class=CliniDetailcSerializer
    permission_classes=[IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
        
    def perform_create(self,serializer):
        serializer.save(doctor_profile=self.request.user.profile)           
        
        
class ReservationsList(ListCreateAPIView):    
    serializer_class=ReserveSerializer   
    permission_classes=[IsAuthenticatedOrReadOnly]
             
    def get_queryset(self):   
        qs=Reservation.objects.all().order_by('-id')
        return qs  
                   
    def post(self,request,format=None):  
        if request.user.is_authenticated and request.user.profile.type == 'patient':
            serializer = ReserveSerializer(data=request.data)
            if serializer.is_valid():          
                clinic=serializer.data["clinic"]     
                try:   
                   clinics=Clinic.objects.get(id=clinic)
                   if Reservation.objects.filter(patient=request.user,doctor=clinics.doctor,clinic=clinics).exists():
                        return Response({"message": "you already have an appointment"})    
                   Reservation.objects.create(doctor=clinics.doctor    
                    ,clinic_id=serializer.data["clinic"],patient=request.user,
                        time=serializer.data["time"],)  
                   return Response(serializer.data)    
                except:    
                    return Response({"message": "invalid doctor"})    
            else:          
                return Response({"message": "invalid data"})    
        else:  
            return Response({"message": "your are not a patient"})   
class Reservations_deatils(RetrieveUpdateDestroyAPIView):
    queryset=Reservation.objects.all()
    lookup_field="id"  
    serializer_class=ReserveSerializer  
    permission_classes=[IsAuthenticatedOrReadOnly,IsPatientOrReadOnly]
     
    def perform_create(self,serializer):
        serializer.save(patient=self.request.user)    

      