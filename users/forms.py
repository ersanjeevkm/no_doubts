from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms
from django.core.exceptions import ValidationError

current_user = None
def crnt_user(user):
    global current_user
    current_user = user

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).first():
            raise ValidationError('This Email-Id already exists! ')
        else:
            return email


class AccountForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).first() and username != current_user.username:
            raise ValidationError('This Username already exists! ')
        else:
            return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).first() and email != current_user.email:
            raise ValidationError('This Email-Id already exists! ')
        else:
            return email

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['notifications', 'field', 'image']
