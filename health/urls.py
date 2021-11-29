from django.urls import path, include
from health import views 
from django.conf.urls import url


urlpatterns = [
    #path('', views.home, name= 'home'),
    path('', views.Home.as_view(), name='home'),
    path('record/<int:pk>', views.Record.as_view(), name='record'),
    path('appointment/', views.Appointment.as_view(), name='appointment'),
    path('appointmentupdate/<int:pk>', views.AppointmentUp.as_view(), name='appointment-update'),
]