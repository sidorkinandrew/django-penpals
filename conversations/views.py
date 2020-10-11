from django.http import request
from pages.models import Profile
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Chat, ChatMember, Message
from .forms import MessageForm
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

        if 'friends_profile' in kwargs and kwargs['friends_profile'] is not None:
            friend_to_chat = self.friends.filter(id=kwargs['friends_profile']).first()
            new_chat_with_friend = Chat()
            new_chat_with_friend.save()
            me_as_chat_member = ChatMember(chat=new_chat_with_friend, profile=self.instance, last_viewed=timezone.now())
            me_as_chat_member.save()
            my_friend_as_chat_member = ChatMember(chat=new_chat_with_friend, profile=friend_to_chat, last_viewed=timezone.now())
            my_friend_as_chat_member.save()


        my_chat_ids = self.instance.chats.all().values_list('chat_id', flat=True)  # all chat ids for my profile in a flat list
        my_chat_objects = Chat.objects.filter(id__in=my_chat_ids)  # all chats ids i'm in 
        im_chatting_with = []

        for a_chat in my_chat_objects:
            a_chat_profile = a_chat.members.get(profile=self.instance)  # get me
            if not a_chat_profile.deleted:
                my_friend_in_a_chat = a_chat.members.exclude(profile=self.instance).first()  # NO GROUP CHATS??? / exclude me from the list of chat memebers
                im_chatting_with.append(my_friend_in_a_chat)  # adding this user/profile to ongoing chats
                self.friends = self.friends.exclude(user=my_friend_in_a_chat.profile.user)  # exclude the freind i'm already chatting with

        self.context = {
            'profile': self.instance,
            'friends': self.friends,
            'chat_details': im_chatting_with,
        }
        return self.context

    def get(self, request, **kwargs):
        self.get_context_data(**kwargs)
        print(self.context, kwargs)
        return render(request, self.template_name, self.context)

#    def get_object(self):
#        return Profile.objects.get(id=self.user.profile.id) #  self.kwargs['profile_id'])


class ChatBox(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    # TemplateDoesNotExist conversations/chat_form.html
    def get_object(self, **kwargs):
        return Chat.objects.get(id=self.kwargs['chat_id']) #  self.kwargs['profile_id'])

