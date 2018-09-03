from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                akun_salah = 'Username atau password salah !'
                return render(request, 'accounts/login.html', {'form':form, 'akun_salah':akun_salah})
    else :
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form':form})


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']
            user = User.objects.create_user(username=username, email=email, password=password_confirm)
            messages.success(request, 'Terimakasih sudah mendaftar, {}'.format(user.username))
            return redirect('login_user')
    else :
        form = RegisterUserForm()
    return render(request, 'accounts/register_user.html', {'form':form})


@login_required
def logout_user(request):
    logout(request)
    return redirect('login_user')






#
