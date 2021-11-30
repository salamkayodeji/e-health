from django.urls import path, include
from health import views 
from django.conf.urls import url


urlpatterns = [
    #path('', views.home, name= 'home'),
    path('', views.Home.as_view(), name='home'),
    path('record/<int:pk>', views.Record.as_view(), name='record'),
    path('appointment/', views.Appointment_create.as_view(), name='appointment'),
    path('appointment/accept/<int:pk>', views.appointment_accept, name='appointment-accept'),
    path('appointment/decline/<int:pk>', views.appointment_decline, name='appointment-decline'),
#    path('appointmentupdate/<int:pk>', views.AppointmentUp.as_view(), name='appointment-update'),
]