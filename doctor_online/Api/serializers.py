from rest_framework import serializers
from doctors.models import *
from rest_framework.serializers import HyperlinkedIdentityField,ModelSerializer


clinic_detail_url = HyperlinkedIdentityField(view_name='api:details',lookup_field="id")
class ClinicSerializer(serializers.ModelSerializer):
	# doctor=serializers.CharField(read_only=True,)
	details = clinic_detail_url 
	class Meta:
		model = Clinic
		fields ='__all__'     
  
class CliniDetailcSerializer(serializers.ModelSerializer):
	doctor=serializers.CharField(read_only=True,)

	class Meta:
		model = Clinic
		fields ='__all__'    
		# exclude=["doctor",]
  
reserve_detail_url = HyperlinkedIdentityField(view_name='api:reserve_details',lookup_field="id")
class ReserveSerializer(serializers.ModelSerializer):
	patient=serializers.CharField(read_only=True,)
	doctor=serializers.CharField(read_only=True,)   
	# details=clinic_detail_url 
	class Meta:
		model = Reservation   
		fields ='__all__'   
  


