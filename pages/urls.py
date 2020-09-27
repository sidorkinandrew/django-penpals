from django.urls import path, include
from .views import SignUpView, index # HomeView

app_name = 'pages'

urlpatterns = [
    path("",  index, name="index"),
    path("signup/", SignUpView.as_view(), name="signup"),
]
