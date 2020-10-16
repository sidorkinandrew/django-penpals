from django.urls import path
from .views import *

app_name = 'conversations'

urlpatterns = [
    path("inbox/", Inbox.as_view(), name="inbox"),
    path("inbox/<int:friends_profile>", Inbox.as_view(), name="inbox_new_chat"),
    path("chatbox/<int:chat_id>", ChatBox.as_view(), name="chatbox"),
    path("delete/chat/<int:chat_id>", ChatBox.delete_chat, name="delete_chat"),
    path("delete/message/<int:message_id>", ChatBox.delete_message, name="delete_message"),
]
