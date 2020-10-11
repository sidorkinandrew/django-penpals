from django.http import request
from pages.models import Profile
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Chat, ChatMember, Message
from pages.models import Profile
from django.urls import reverse_lazy, reverse

from django.utils import timezone

# Create your views here.

class Inbox(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "conversations/inbox.html"

    def get_context_data(self, **kwargs):
        self.instance = self.request.user.profile
        self.friends = self.instance.friends.all()
        print("kwargs", kwargs)  # friends_profile

        if 'friends_profile' in kwargs and kwargs['friends_profile'] is not None:
            friend_to_chat = self.friends.filter(id=kwargs['friends_profile']).first()
            new_chat_with_friend = Chat()
            new_chat_with_friend.save()
            me_as_chat_member = ChatMember(chat=new_chat_with_friend, profile=self.instance, last_viewed=timezone.now())
            me_as_chat_member.save()
            my_friend_as_chat_member = ChatMember(chat=new_chat_with_friend, profile=friend_to_chat, last_viewed=timezone.now())
            my_friend_as_chat_member.save()
            print(friend_to_chat, new_chat_with_friend, me_as_chat_member, my_friend_as_chat_member)


        my_chat_ids = self.instance.chats.all().values_list('chat_id', flat=True)
        my_chat_objects = Chat.objects.filter(id__in=my_chat_ids)
        print(my_chat_ids)
        print(my_chat_objects)

        self.context = {
            'profile': self.instance,
            'friends': self.friends,
        }
        return self.context

    def get(self, request, **kwargs):
        self.get_context_data(**kwargs)
        print(self.context, kwargs)
        return render(request, self.template_name, self.context)

#    def get_object(self):
#        return Profile.objects.get(id=self.user.profile.id) #  self.kwargs['profile_id'])

