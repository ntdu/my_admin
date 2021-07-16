from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from user.models import Investor 


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
        label="Họ và tên", 
        required=True, 
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Họ và tên",                
                "class": "form-control"
            }
        ))

    phone = forms.CharField(
        label="Số điện thoại", 
        required=True, 
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Số điện thoại",                
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
            print("password1")
            
            return False

        if User.objects.filter(username=self.data.get('phone')).exists():
            self.errors['phone'] = "Số điện thoại đã tồn tại"
            print("phone")
            
            return False

        return True


    def save(self):
        id =  int(self.data.get('id', '0'))        
        return self.create() if id == 0 else self.update(id)

    def create(self):
        user = User.objects.create_user(
            self.data.get('phone'),
            self.data.get('email'),
            self.data.get('password1')       
        )
        user.save()

        investor = Investor(
            name = self.data.get('username'),
            login_account =  user
        )
        investor.save()

    
    def update(self, id):
        user = User.objects.get(id=self.data.get('id'))

        user.username = self.data.get('phone')
        user.email = self.data.get('email')
        user.password = self.data.get('password1')
        user.save()

    
