from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

from .forms import RegisterUser, LoginUser, CreateSite
from .models import User, Site


def main(request):
    context = {
        'title': 'Main Page'
    }
    return render(request, "vpn_service/main.html", context)


@login_required(login_url='login')
def create_site(request):
    context = {
        'title': 'Create site',
        'create_site_form': CreateSite
    }

    if request.method == "POST":
        site = CreateSite(request.POST)

        if site.is_valid():
            site_instance = site.save(commit=False)
            site_instance.user = request.user
            site_instance.save()

    return render(request, 'vpn_service/create_site.html', context)


@login_required(login_url='login')
def personal_cabinet(request):
    context = {
        'title': 'Personal Cabinet',
        'sites': Site.objects.filter(user=request.user),
        'statistics': request.user.statistics
    }

    return render(request, "vpn_service/personal_cabinet.html", context)


def register_user(request):
    context = {
        'title': 'Registration form',
        'register_form': RegisterUser
    }

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if User.objects.filter(username=username):
            messages.error(request, "This username is already used!")
            return redirect('registration')

        if password != password_confirm:
            messages.error(request, "The passwords don't match")
            return redirect('registration')

        user = User.objects.create(username=username, password=make_password(password))
        login(request, user)
        return redirect('main')

    return render(request, 'vpn_service/register.html', context)


def login_user(request):
    context = {
        'title': 'Login form',
        'login_form': LoginUser
    }

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "You have been successfully logged in!")
            return redirect(request.GET.get('next', 'main'))
        else:
            messages.error(request, "Wrong username or password")
            return redirect('login')

    return render(request, 'vpn_service/login.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out!")
    return redirect('main')
