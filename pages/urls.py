from django.urls import path, include
from .views import * # HomeView

app_name = 'pages'

urlpatterns = [
    path("",  HomeView.as_view(), name="index"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('profile/<int:profile_id>', ProfileView.as_view(), name="profile"),
    path("edit", ProfileEdit.as_view(), name="edit"),
    path("search", ProfileSearch.as_view(), name="search"),
    path("request/send/<int:to_profile_id>", ProfileView.send_request, name="send_request"),
    path("request/cancel/<int:to_profile_id>", ProfileView.cancel_request, name="cancel_request"),
    path("request/accept/<int:from_profile_id>", ProfileView.accept_friend_request, name="accept_request"),    
]
