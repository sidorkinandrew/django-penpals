from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from .models import Chat, ChatMember, Message

# Create your views here.

class Inbox(DetailView):
    model = Chat

