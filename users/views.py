from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse

from .models import UserProfile
from .forms import RegistrationForm, UserCreationForm


class RegistrationView(CreateView):
    template_name = 'users/register.html'
    form_class = RegistrationForm
    
    def get_context_data(self, *args, **kwargs):
        context = super(RegistrationView, self).get_context_data(*args, **kwargs)
        return context

    def get_success_url(self):
        success_url = reverse('login')

        return success_url
