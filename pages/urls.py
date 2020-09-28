from django.urls import path, include
from .views import SignUpView, ProfileView, index # HomeView

app_name = 'pages'

urlpatterns = [
    path("",  index, name="index"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('profile/<int:profile_id>', ProfileView.as_view(), name="profile"),
]
