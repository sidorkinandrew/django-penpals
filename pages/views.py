import ast
from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from .models import Profile
from .forms import * # UserRegisterForm, ProfileEditForm, ProfileViewForm
from django.contrib import messages
from .utils import *


class HomeView(DetailView):
    template_name = 'pages/index.html'
    form_class = ProfileViewForm
    context_object_name = 'profile'
    model = Profile
    
    def get_object(self):
        if self.request.user.is_authenticated:
            self.instance = Profile.objects.get(id=self.request.user.profile.id)
#            self.instance.speaks = from_value_to_label(self.instance.speaks)
#            self.instance.learns = from_value_to_label(self.instance.learns)
        else:
            self.instance = Profile.objects.none()
        return self.instance
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        self.users = Profile.objects.all()
        if self.request.user.is_authenticated:
            self.users = self.users.exclude(id=self.request.user.profile.id)
#        for user in self.users:
#            user.speaks = from_value_to_label(user.speaks)
#            user.learns = from_value_to_label(user.learns)

        context.update({
            'users': self.users,
            'profile': self.instance,
        })
        return context

class ProfileView(SuccessMessageMixin, DetailView):
    template_name = 'pages/profile.html'
    form_class = ProfileViewForm
    context_object_name = 'profile'
    model = Profile
    
    def get_object(self): 
        instance = Profile.objects.get(id=self.kwargs['profile_id'])  # self.request.user.profile.id)
        return instance

class ProfileEdit(SuccessMessageMixin, UpdateView):
    model = Profile
    template_name = 'pages/edit.html'
    form_class = ProfileEditForm
    context_object_name = 'profile'
    success_message = "Your profile was updated successfully"  

    def get_object(self):
        return  Profile.objects.get(id=self.request.user.profile.id) #  self.kwargs['profile_id'])

    def get_initial(self):
        initial = {'speaks': from_label_to_value(self.request.user.profile.speaks),
                'learns': from_label_to_value(self.request.user.profile.learns)}
        return initial

    def get_success_url(self):
          profile_id=self.request.user.profile.id
          return reverse_lazy('pages:profile', kwargs={'profile_id': profile_id})

class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'pages/signup.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('pages:index')
    success_message = "Your profile was created successfully"

class ProfileSearch(ListView, HomeView):
    template_name = 'pages/index.html'
    context_object_name = 'users'
    model = Profile
    instance = Profile.objects.none()
    users = Profile.objects.none()

    def get_queryset(self):
        query_speaks = from_label_to_value(self.request.GET.get('speaks'))
        print('query_speaks:',query_speaks, self.request.GET.get('speaks'))
        query_learns = from_label_to_value(self.request.GET.get('learns'))
        print('query_learns:',query_learns, self.request.GET.get('learns'))
        self.users = Profile.objects.none()
        for language in query_speaks:
            self.users |= Profile.objects.filter(speaks__icontains=language)
        for language in query_learns:
            self.users |= Profile.objects.filter(learns__icontains=language)
        if (not self.request.GET.get('speaks')) and (not self.request.GET.get('learns')):
            self.users = Profile.objects.all()
        print(self.users)
        return self.users

    def get_context_data(self, **kwargs):
        self.instance = self.get_object()
        if self.request.user.is_authenticated:
            self.users = self.users.exclude(id=self.request.user.profile.id)
        context = {
            'users': self.users,
            'profile': self.instance,
        }
        return context
    

