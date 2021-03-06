from django.contrib.auth import authenticate, login
from django.http import request
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy, reverse
from .models import FriendRequest, Profile
from .forms import * # UserRegisterForm, ProfileEditForm, ProfileViewForm
from django.contrib import messages
from .utils import *
from django.core.paginator import Paginator


class HomeView(DetailView):
    template_name = 'pages/index.html'
    form_class = ProfileViewForm
    context_object_name = 'profile'
    model = Profile
    users = Profile.objects.none()
    objects_per_page = 8

    def get_object(self):
        if self.request.user.is_authenticated:
            self.instance = Profile.objects.get(id=self.request.user.profile.id)
        else:
            self.instance = Profile.objects.none()
        return self.instance
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        self.users = Profile.objects.all()
        if self.request.user.is_authenticated:
            self.users = self.users.exclude(id=self.request.user.profile.id)

        page_number = self.request.GET.get('page')
        paginator_object = Paginator(self.users, self.objects_per_page)
        page_object = paginator_object.get_page(page_number)

        context.update({
            'page_object': page_object,  # self.users,
            'profile': self.instance,
        })
        return context

class ProfileView(SuccessMessageMixin, DetailView):
    template_name = 'pages/profile.html'
    form_class = ProfileViewForm
    context_object_name = 'profile'
    model = Profile
    friends = Profile.objects.none()
    instance = Profile.objects.none()
    
    def get_object(self): 
        self.instance = Profile.objects.get(id=self.kwargs['profile_id'])  # self.request.user.profile.id)
        self.friends = FriendRequest.objects.filter(to_profile = self.instance)
        return self.instance
    
    def get_context_data(self, **kwargs):
        self.friends = self.instance.friends.all()
        received_requests = FriendRequest.objects.filter(to_profile = self.instance)
        outgoing_requests = self.instance.from_profile.all()
        button_friend_text = ""
        if self.request.user.is_authenticated:
            if self.request.user.profile not in self.friends:
                button_friend_text = "not_friend_yet"
                if len(FriendRequest.objects.filter(from_profile = self.request.user.profile).filter(to_profile=self.instance))==1:
                    button_friend_text = "request_sent"
#        print("get_context_data 1: ", self.friends, received_requests)
#        print("get_context_data 2: ", self.request.user.is_authenticated, self.request.user.profile)
#        print("get_context_data 3: ", FriendRequest.objects.filter(from_profile = self.request.user.profile).filter(to_profile=self.instance))
        self.context_data = {
            'profile': self.instance,
            'friends': self.friends,
            'received_requests': received_requests,
            'outgoing_requests': outgoing_requests,
            'button_friend_text': button_friend_text,
        }
        return self.context_data

    def withdraw_request(self, profile_id):
        profile_to_unfriend = Profile.objects.get(pk=profile_id)
        instance = self.user.profile
        instance.friends.remove(profile_to_unfriend)
        return redirect('pages:profile', profile_id = instance.id)
    
    def send_request(self, to_profile_id):
        print('send_request', self.user, to_profile_id)
        if self.user.is_authenticated:
            to_profile = Profile.objects.get(pk=to_profile_id)
            self.friends = FriendRequest.objects.get_or_create(
                from_profile = self.user.profile,
                to_profile = to_profile
            )
        return redirect('pages:profile', profile_id = to_profile_id)
        #return redirect(reverse('pages:profile', kwargs={ 'profile_id': to_profile_id }))

    def cancel_request(self, to_profile_id):
        print('cancel_request', self.user, to_profile_id)
        if self.user.is_authenticated:
            to_profile = Profile.objects.get(pk=to_profile_id)
            request_sent = FriendRequest.objects.filter(
                from_profile = self.user.profile,
                to_profile = to_profile
            ).first()
            request_sent.delete()
        return redirect('pages:profile', profile_id = to_profile_id)  # redirect(reverse('pages:profile', kwargs={ 'profile_id': to_profile_id }))

    def drop_friend_request(self, to_profile_id):
        print('drop_request', self.user, to_profile_id)
        if self.user.is_authenticated:
            to_profile = Profile.objects.get(pk=to_profile_id)
            request_sent = FriendRequest.objects.filter(
                from_profile = self.user.profile,
                to_profile = to_profile
            ).first()
            print(request_sent, 'to be deleted')
            request_sent.delete()
        return redirect('pages:profile', profile_id = self.user.profile.id)  # redirect(reverse('pages:profile', kwargs={ 'profile_id': to_profile_id }))

    def accept_friend_request(self, from_profile_id):
        print('accept_friend_request', self.user, from_profile_id)
        from_profile = Profile.objects.get(pk=from_profile_id)
        to_profile = self.user.profile
        request_received = FriendRequest.objects.filter(
                from_profile = from_profile_id,
                to_profile = self.user.profile,
            ).first()
        friend_to = request_received.to_profile
        friend_from = from_profile
        friend_to.friends.add(friend_from)
        request_received.delete()
        print(friend_to, friend_from, friend_to.friends)
        return redirect('pages:profile', profile_id = to_profile.id)  # redirect(reverse('pages:profile', kwargs={ 'profile_id': to_profile_id }))

    def delete_friend_request(self, from_profile_id):
        print('delete_friend_request', self.user, from_profile_id)
        from_profile = Profile.objects.get(pk=from_profile_id)
        to_profile = self.user.profile
        request_received = FriendRequest.objects.filter(
                from_profile = from_profile_id,
                to_profile = self.user.profile,
            ).first()
        request_received.delete()
        return redirect('pages:profile', profile_id = self.user.profile.id)


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
    def form_valid(self, form):
        return_page = super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)
        return return_page


class ProfileSearch(ListView, HomeView):
    template_name = 'pages/index.html'
    context_object_name = 'page_object'
    model = Profile
    instance = Profile.objects.none()
    users = Profile.objects.none()
    objects_per_page = 8

    def get_queryset(self):
        query_speaks = from_label_to_value(self.request.GET.get('speaks'))
        query_learns = from_label_to_value(self.request.GET.get('learns'))
        self.users = Profile.objects.none()
        self.search_query = f"speaks={self.request.GET.get('speaks')}&learns={self.request.GET.get('learns')}&"
        for id, language in enumerate(query_speaks):
            if id == 0:
                self.users = Profile.objects.filter(speaks__icontains=language)
            else:
                self.users = self.users.filter(speaks__icontains=language)
        for id, language in enumerate(query_learns):
            if id == 0 and self.users.count() == 0:
                self.users = Profile.objects.filter(learns__icontains=language)
            else:
                self.users = self.users.filter(learns__icontains=language)
        if (not self.request.GET.get('speaks')) and (not self.request.GET.get('learns')):
            self.users = Profile.objects.all()
        return self.users

    def get_context_data(self, **kwargs):
        self.instance = self.get_object()
        if self.request.user.is_authenticated:
            self.users = self.users.exclude(id=self.request.user.profile.id)
        
        page_number = self.request.GET.get('page')
        paginator_object = Paginator(self.users, self.objects_per_page)
        page_object = paginator_object.get_page(page_number)
        
        context = {
            'page_object': page_object, #self.users,
            'profile': self.instance,
            'search_query': self.search_query,
        }
        return context
    