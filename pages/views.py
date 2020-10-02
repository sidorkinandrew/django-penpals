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
from .utils import LANGUAGE_CHOICES, from_value_to_label


class HomeView(DetailView):
    template_name = 'pages/index.html'
    form_class = ProfileViewForm
    context_object_name = 'profile'
    model = Profile
    
    def get_object(self):
        if self.request.user.is_authenticated:
            self.instance = Profile.objects.get(id=self.request.user.profile.id)
            self.instance.speaks = from_value_to_label(self.instance.speaks)
            self.instance.learns = from_value_to_label(self.instance.learns)
        else:
            self.instance = Profile.objects.none()
        return self.instance
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        self.users = Profile.objects.all()
        if self.request.user.is_authenticated:
            self.users = self.users.exclude(id=self.request.user.profile.id)
        for user in self.users:
            user.speaks = from_value_to_label(user.speaks)
            user.learns = from_value_to_label(user.learns)

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
        instance.speaks = from_value_to_label(instance.speaks)
        instance.learns = from_value_to_label(instance.learns)
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
        return {'speaks': ast.literal_eval(self.request.user.profile.speaks),
                'learns': ast.literal_eval(self.request.user.profile.learns)}

    def get_success_url(self):
          profile_id=self.request.user.profile.id
          return reverse_lazy('pages:profile', kwargs={'profile_id': profile_id})

class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'pages/signup.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('pages:index')
    success_message = "Your profile was created successfully"

class SearchForm(DetailView):
    template_name = 'pages/index.html'
    form_class = SearchForm
    context_object_name = 'profile'
    model = Profile
    profiles = []
    
    def get_queryset(self):
        form = self.form_class(self.request.GET)
        print(form)
        if form.is_valid():
            return Profile.objects.filter(speaks__icontains=form.cleaned_data['speaks'])
        return Profile.objects.all()
