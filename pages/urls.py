from django.urls import path, include
from .views import HomeView, SignUpView

app_name = 'pages'

urlpatterns = [
    path("",  HomeView.as_view(), name="index"),
    path("signup/", SignUpView.as_view(), name="signup"),
]
