from django import forms
from .models import Appointment


        
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patientid', 'docterid', 'appointment_date', 'status',]