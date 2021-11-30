from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from users.models import UserProfile, Medical_History
from .models import Appointment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import *
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


def is_valid_queryparam(param):
    return param != '' and param is not None

# Create your views here.
class Home(LoginRequiredMixin, ListView):
    model = Medical_History    
    template_name = 'health/home.html'
    context_object_name = 'posts'
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        pizza = self.request.GET.get('ailment')
        if pizza:
            return qs.filter(ailment=pizza)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        appoint = Appointment.objects.values_list("appointment_date").filter(docterid = self.request.user)
        context['appoint'] = Appointment.objects.filter(docterid = self.request.user)
        context['accept'] = Appointment.objects.filter(docterid = self.request.user, status = 'ACCEPTED').count()
        context['decline'] = Appointment.objects.filter(docterid = self.request.user, status = 'DECLINED').count()
        #month = Appointment.objects.filter(docterid = self.request.user, appointment_date__month = 12).count()
        #month = Appointment.objects.filter(docterid = self.request.user, appointment_date__range=[Appointment.appointment_date, Appointment.appointment_date]).count()       
        #print(month)
        # And so on for more models
        return context
   

    
    

    

class Record(LoginRequiredMixin, UpdateView):
    model = Medical_History    
    fields = ['gender', 'date_of_birth', 'address', 'age', 'blood', 'ailment']
    template_name = 'health/records.html'
    
    def get_form(self):
        form = super().get_form()
        form.fields['date_of_birth'].widget=forms.widgets.DateInput(
            attrs={'placeholder': 'Date of Birth', 'type': 'text',
                   'onfocus': "(this.type='date')", }
        )
        return form
    
    def form_valid(self, form):
        form.instance.email = self.request.user
        return super().form_valid(form)

class Appointment_create(LoginRequiredMixin, CreateView):
    model = Appointment
    template_name = 'health/appointment.html'
    fields = ['docterid', 'appointment_date']

    def get_form(self):
        form = super().get_form()
        form.fields['appointment_date'].widget=forms.widgets.DateInput(
            attrs={'placeholder': 'Appointment', 'type': 'text',
                   'onfocus': "(this.type='date')", }
        )
        form.fields["docterid"].queryset = UserProfile.objects.filter(category='DOCTOR')
        
        return form
    def form_valid(self, form):
        form.instance.patientid = self.request.user
        form.instance.status = 'PENDING'
#       print(self.request.POST.get('doctorid'))
#       form.instance.docterid = self.request.POST.get('doctorid')
        subject = 'APPOINTMENT'
        message = f'Patient {self.request.user}, has booked an appointment with you for {form.instance.appointment_date}'
        email_from = settings.EMAIL_HOST_USER
        to = [form.instance.docterid]
        print(to)
        send_mail(subject, message, email_from, to, fail_silently=False)

        return super().form_valid(form)
    
    

#class AppointmentUp(LoginRequiredMixin, UpdateView):
#    model = Appointment
#    template_name = 'health/appointment.html'
#    fields = ['status']
    
#    def form_valid(self, form):
#        form.instance.status = self.request.GET.get('status')
                        
#        return super().form_valid(form)
def appointment_decline(request, pk):
    post = Appointment.objects.get(pk=pk)
    post.patientid 
    post.docterid 
    post.appointment_date
    post.status = 'DECLINED'
    print(post.status)
    post.save()
    return redirect('home')


def appointment_accept(request, pk):
    post = Appointment.objects.get(pk=pk)
    post.patientid 
    post.docterid 
    post.appointment_date
    post.status = 'ACCEPTED'
    print(post.status)
    post.save()
    return redirect('home')

 #       post.appointment_date= request.POST.get('appointment_date')


#def appointment(request):
#    doctor = UserProfile.objects.all()
#    form = AppointmentForm()
#    if request.method == 'POST':
#        post = form.save()
#        print(form.docterid)
#        post.refresh_from_db()
#        post.patientid= request.user
##        post.docterid= request.POST.get('docterid')
 #       print(post.docterid)
 #       post.appointment_date= request.POST.get('appointment_date')
#        post.status= 'PENDING'
#        post.save() 
#        messages.success(request, f'Your appointment as been booked for {post.appointment_date}')
#    return render(request, 'health/appointment.html', {'doctor':doctor, 'form':form}) 


