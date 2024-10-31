from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginUser(AuthenticationForm):
    Indentifier = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    
    