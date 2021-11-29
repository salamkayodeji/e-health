from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from users.models import UserProfile, Medical_History
from .models import Appointment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import *
from django.contrib import messages

def is_valid_queryparam(param):
    return param != '' and param is not None

# Create your views here.
class Home(LoginRequiredMixin, ListView):
    model = Medical_History    
    template_name = 'health/home.html'
    context_object_name = 'posts'
    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        # And so on for more models
        return context
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        pizza = self.request.GET.get('ailment')
        if pizza:
            return qs.filter(ailment=pizza)
        return qs

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

class Appointment(LoginRequiredMixin, CreateView):
    model = Appointment
    template_name = 'health/appointment.html'
    fields = ['appointment_date']

    def get_context_data(self, **kwargs):
        context = super(Appointment, self).get_context_data(**kwargs)
        context['doctor'] = UserProfile.objects.all()
        return context

    
    def get_form(self):
        form = super().get_form()
        form.fields['appointment_date'].widget=forms.widgets.DateInput(
            attrs={'placeholder': 'Appointment', 'type': 'text',
                   'onfocus': "(this.type='date')", }
        )
        return form
    def form_valid(self, form):
        form.instance.patientid = self.request.user
        form.instance.status = 'PENDING'
        num = int(self.request.POST.get('doctorid'))
        print(type(num))
        form.instance.docterid = num
        return super().form_valid(form)
    

class AppointmentUp(LoginRequiredMixin, UpdateView):
    model = Appointment
    template_name = 'health/appointment.html'
    fields = ['STATUS']
    
    def form_valid(self, form):
        if form.instance.status == 'ACCEPT':
            form.instance.status = 'ACCEPT'
        else:
            form.instance.status = 'DECLINE'            
        return super().form_valid(form)


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

