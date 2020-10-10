from django.contrib import admin

# Register your models here.

from .models import Chat, ChatMember, Message


admin.site.register(Chat)
admin.site.register(ChatMember)
admin.site.register(Message)
