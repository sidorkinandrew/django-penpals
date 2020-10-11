from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    content = forms.CharField(max_length=500, required=True)

    class Meta:
        model = Message
        fields = ['content']
