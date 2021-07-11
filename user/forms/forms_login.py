from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Tên đăng nhập", 
        required=True, 
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Tên đăng nhập",                
                "class": "form-control"
            }
        ))
    
    password = forms.CharField(
        label="Password", 
        required=True, 
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Mật khẩu",                
                "class": "form-control"
            }
        ))