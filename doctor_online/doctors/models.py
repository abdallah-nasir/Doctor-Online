from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
# Create your models here.

TYPE=(
    ("doctor","doctor"),
    ("patient","patient")
)
DAYS=(
    ('Saturday',"Saturday"),
    ('Sunday',"Sunday"),
    ('Monday',"Monday"),
    ('Tuesday',"Tuesday"),
    ('Wednesday',"Wednesday"),
    ('Thursday',"Thursday"),
    ('Friday',"Friday"),

)
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    type=models.CharField(choices=TYPE,max_length=20)

    def __str__(self):
        return self.user.username
  
class Clinic(models.Model):
    doctor=models.ForeignKey(Profile,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    price=models.PositiveIntegerField()
    days=MultiSelectField(choices=DAYS)
    start_time=models.TimeField(auto_now_add=False)
    end_time=models.TimeField(auto_now_add=False)    
                            
    def __str__(self):
        return self.doctor.user.username
    
    def this_reservations(self):   
        reserve=Reservation.objects.filter(clinic=self.clinic)
        context={"reserve":reserve}
        return context


class Reservation(models.Model):
    doctor=models.ForeignKey(Profile,on_delete=models.CASCADE)
    clinic=models.ForeignKey(Clinic,on_delete=models.CASCADE)
    patient=models.ForeignKey(User,on_delete=models.CASCADE)
    time=models.TimeField(auto_now_add=False)    

    def __str__(self):
        return self.patient.username