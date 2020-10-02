from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm 
from .utils import LANGUAGE_CHOICES
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileViewForm(UserChangeForm, forms.ModelForm):
    first = forms.CharField(max_length=100, required=True)
    last = forms.CharField(max_length=100, required=True)
    speaks = forms.MultipleChoiceField(choices=LANGUAGE_CHOICES, required=True)
    learns = forms.MultipleChoiceField(choices=LANGUAGE_CHOICES, required=True)

    class Meta:
        model = Profile
        fields = ['first', 'last', 'speaks', 'learns', 'photo']


class ProfileEditForm(UserChangeForm, forms.ModelForm):
    first = forms.CharField(max_length=100, required=True)
    last = forms.CharField(max_length=100, required=True)
    speaks = forms.MultipleChoiceField(choices=LANGUAGE_CHOICES, required=True)
    learns = forms.MultipleChoiceField(choices=LANGUAGE_CHOICES, required=True)

    class Meta:
        model = Profile
        fields = ['first', 'last', 'speaks', 'learns', 'photo']

class SearchForm(forms.ModelForm):
    speaks = forms.CharField(max_length=100, required=True)
    learns = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Profile
        fields = ['speaks', 'learns']