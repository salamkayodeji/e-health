from django.db import models
from django.urls import reverse


# Create your models here.
STATUS = (
    ('PENDING', 'PENDING'),
    ('ACCEPTED', 'ACCEPTED'),
    ('DECLINED', 'DECLINED')
)

class Appointment(models.Model):
    patientid = models.ForeignKey('users.UserProfile', on_delete = models.CASCADE, blank=True,null=True)
    docterid = models.ForeignKey('users.UserProfile', related_name="doctor", on_delete = models.CASCADE, blank=True,null=True)
    time = models.DateTimeField(auto_now_add=True)
    appointment_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length = 20, choices=STATUS)
    
    def get_absolute_url(self):
        return reverse("appointment")
        
    def __str__(self):
        return str(self.patientid)

    
    
