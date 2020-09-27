from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Profile
from .forms import UserRegisterForm
from django.contrib import messages

# Create your views here.
class HomeView(LoginRequiredMixin, ListView):
    template_name = 'pages/index.html'
    model = Profile

class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'pages/signup.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('pages:index')
    success_message = "Your profile was created successfully"