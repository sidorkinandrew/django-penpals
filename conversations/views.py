from django.http import request
from pages.models import Profile
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Chat, ChatMember, Message
from pages.models import Profile
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect

# Create your views here.

class Inbox(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "conversations/inbox.html"

    def get_context_data(self, **kwargs):
        self.instance = self.request.user.profile
        self.friends = self.instance.friends.all()
        self.context = {
            'profile': self.instance,
            'friends': self.friends,
        }
        return self.context

    def get(self, request):
        self.get_context_data()
        print(self.context)
        return render(request, self.template_name, self.context)

#    def get_object(self):
#        return Profile.objects.get(id=self.user.profile.id) #  self.kwargs['profile_id'])
