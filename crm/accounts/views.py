from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password

from .models import User
from .auth_user import UserAuth as auth


def login_page(req):
    messages = []
    if req.method == 'POST':
        user = auth.authenticate(phone=req.POST['phone'], password=req.POST['passwd'])
        if user == None:
            messages.append('Неверный логин или пароль, пожалуйста проверте правильность заполнения полей и попробуйте снова!')
        else:
            login(req, user)
            return redirect('main', 'manage')

    if req.user.is_authenticated:
        return redirect('main', 'manage')
    else:
        return render(req, 'accounts/login.html', {'messages': messages})


def logoutView(req):
    logout(req)
    return redirect('login')