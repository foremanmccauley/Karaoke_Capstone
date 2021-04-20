from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SearchForm(forms.Form):
    keywords = forms.CharField(label='Search for a song here', max_length=255)

class MP3Form(forms.Form):
    song = forms.FileField(label='MP3 file here', required=False)
    video = forms.FileField(label='WEBM file here', required=False)