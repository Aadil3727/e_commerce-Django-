from django import forms
from . import models
from .models import Auth_user

class Sign_Up(forms.ModelForm):
    
    class Meta:
        model = Auth_user
        fields = ['username','email','password','image','phone_no']

class Login_User(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
