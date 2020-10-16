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

class Inbox(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "conversations/inbox.html"

    def get_context_data(self, **kwargs):
        self.instance = self.request.user.profile
        self.friends = self.instance.friends.all()
        self.context = {
            'profile': self.instance,
            'friends': self.friends,
        }

        if 'friends_profile' in kwargs and kwargs['friends_profile'] is not None:
            friend_to_chat = self.friends.filter(id=kwargs['friends_profile']).first()
            chats_deleted = ChatMember.objects.filter(profile=self.instance, deleted=True).values_list('chat_id', flat=True)
            if chats_deleted:
                chat_with_friend = ChatMember.objects.filter(chat_id__in=chats_deleted, profile_id=friend_to_chat.id).first()

                if chat_with_friend:
                    member_to_undelete = ChatMember.objects.get(chat_id=chat_with_friend.chat_id, profile=self.instance)
                    member_to_undelete.deleted = False
                    member_to_undelete.save()
                else:
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
        print(self.context, request, kwargs)
        return render(request, self.template_name, self.context)

#    def get_object(self):
#        return Profile.objects.get(id=self.user.profile.id) #  self.kwargs['profile_id'])


class ChatBox(LoginRequiredMixin, DetailView):
    model = Message
    form_class = MessageForm
    template_name = "conversations/chatbox.html"
    # TemplateDoesNotExist conversations/chat_form.html

    def get_context_data(self, **kwargs):
        self.instance = self.request.user.profile
        self.messages = Message.objects.all().filter(chat_id=self.kwargs['chat_id']) #  self.kwargs['profile_id'])

        self.context = {
            'profile': self.instance,
            'chat_id': self.kwargs['chat_id'],
            'form': self.form_class,
            'chat_messages': self.messages,
        }
        print(self.context)
        return self.context

    def post(self, request, **kwargs):
        self.get_context_data(**kwargs)
        self.chat_id = self.kwargs['chat_id']
        self.form = MessageForm(request.POST)
        new_message = self.form.save(commit=False)
        new_message.profile = self.instance
        new_message.chat_id = self.kwargs['chat_id']
        new_message.save()
        messages = Message.objects.filter(chat_id=self.chat_id)
        last_viewed = ChatMember.objects.filter(chat_id=self.chat_id).filter(profile=self.instance)
        last_viewed.update(last_viewed = timezone.now())
        return redirect('conversations:chatbox', chat_id=self.chat_id)
    
    def delete_chat(self, **kwargs):
        self.chat_id = kwargs['chat_id']
        chat_to_delete = Chat.objects.get(id=self.chat_id)
        chat_members = chat_to_delete.members.all()
        me_in_the_chat, friends_in_the_chat = "", ""
        for amember in chat_members:
            if amember.profile == self.user.profile:
                me_in_the_chat = amember
            else:
                friends_in_the_chat = amember  #friends_in_the_chat.append(amember)

        if not me_in_the_chat.deleted:
            me_in_the_chat.deleted = True
            me_in_the_chat.save()
        
        if friends_in_the_chat.deleted:
            chat_to_delete.save()
        return redirect('conversations:inbox')
    
    def delete_message(self, **kwargs):
        self.message_id = kwargs['message_id']
        message_to_delete = Message.objects.get(id=self.message_id)
        message_to_delete.delete()
        return redirect('conversations:chatbox', chat_id = message_to_delete.chat_id)

    def get_object(self, **kwargs):
        return Message.objects.all().filter(chat_id=self.kwargs['chat_id']) #  self.kwargs['profile_id'])

