from django.utils import path
from .views import *

app_name = 'conversations'

urlpatterns = [
    path("inbox", Inbox.as_view(), name="inbox"),
]
