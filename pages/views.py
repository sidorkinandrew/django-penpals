from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from .models import Profile
from .forms import UserRegisterForm, ProfileEditForm
from django.contrib import messages

def index(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(id=request.user.id)
    else:
        profile = ''
    
    context = {
        'profile': profile
    }

    return render(request,'pages/index.html',context)

#def profile(request, profile_id, *args, **kwargs):
#    profile = Profile.objects.get(id=profile_id)
#    context = {
#        'profile': profile,
#    }
#    return render(request, 'pages/profile.html', context)

class ProfileView(SuccessMessageMixin, DetailView):
    template_name = 'pages/profile.html'
    form_class = ProfileEditForm
    context_object_name = 'profile'
    model = Profile

    def get_object(self):
        return Profile.objects.get(id=self.kwargs['profile_id'])


def edit_profile(request):
    pass
# Create Home (not used)
#class HomeView(LoginRequiredMixin, ListView):
#    template_name = 'pages/index.html'
#    model = Profile

class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'pages/signup.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('pages:index')
    success_message = "Your profile was created successfully"