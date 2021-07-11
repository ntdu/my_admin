from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_length(value):
    if len(value) < 8:
        raise ValidationError(
            _('Mật khẩu phải dài hơn 8 ký tự(hiện tại có %(length)s ký tự!)'),
            params={'length': len(value)},
        )


class CreateUserForm(forms.Form):
    id = forms.IntegerField(
        required=False, 
        widget=forms.HiddenInput())

    username = forms.CharField(
        label="Tên đăng nhập", 
        required=True, 
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Tên đăng nhập",                
                "class": "form-control"
            }
        ))
    
    email = forms.EmailField(
        label="Email", 
        required=False, 
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",                
                "class": "form-control"
            }
        ))
    
    password1 = forms.CharField(
        label="Password", 
        required=True, 
        validators=[validate_length, ],
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Mật khẩu",                
                "class": "form-control"
            }
        ))

    password2 = forms.CharField(
        label="Password  check", 
        required=True, 
        validators=[validate_length, ],
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Nhập lại mật khẩu",                
                "class": "form-control"
            }
        ))

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
    
    def is_valid(self):
        valid = super(CreateUserForm,self).is_valid()

        if self.data.get('password1') != self.data.get('password2'):
            self.errors['password1'] = "Mật khẩu không khớp"
            
            return False

        if User.objects.filter(username=self.data.get('username')).exists():
            self.errors['username'] = "Tên đăng nhập đã tồn tại"
            
            return False


    def save(self):
        id =  int(self.data.get('id', '0'))        
        return self.create() if id == 0 else self.update(id)

    def create(self):
        user = User.objects.create_user(
            self.data.get('username'),
            self.data.get('email'),
            self.data.get('password1')       
        )
        user.save()
    
    def update(self, id):
        user = User.objects.get(id=self.data.get('id'))

        user.username = self.data.get('username')
        user.email = self.data.get('email')
        user.password = self.data.get('password1')
        user.save()

    
