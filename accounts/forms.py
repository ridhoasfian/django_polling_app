from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', min_length=5, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))

class RegisterUserForm(forms.Form):
    username = forms.CharField(label='Username', min_length=5, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'E-Mail'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    password_confirm = forms.CharField(label='Password Confirm', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password Confirm'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        qs = User.objects.filter(username__iexact=username)
        if qs.exists():
            raise ValidationError('Username sudah terdaftar !')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise ValidationError('Email sudah digunakan !')
        return email

    def clean_password_confirm(self):
        password_confirm = self.cleaned_data['password_confirm']
        password = self.cleaned_data['password']
        if password_confirm != password:
            raise ValidationError('Konfirmasi password tidak sama !')
        return password_confirm










    #
