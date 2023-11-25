import decimal
import urllib.parse

import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from . import services
from .forms import RegisterUser, LoginUser, CreateSite, UserProfileForm
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


@csrf_exempt
@login_required(login_url='login')
def site_view(request, site_pk, site_slug, domain_url=''):
    site_obj = get_object_or_404(Site, pk=site_pk)

    if site_obj.user != request.user:
        raise Http404()

    statistics = site_obj.statistics

    url = urllib.parse.urljoin(site_obj.url, domain_url)
    if request.method == "POST":
        headers = dict(request.headers)
        headers['Referer'] = url
        headers['Origin'] = site_obj.url
        resp = requests.post(
            f"{url}?{'&'.join([f'{key}={value}' for key, value in request.GET.items()])}",
            headers=headers,
            cookies=request.COOKIES,
            data=request.POST,
            allow_redirects=False
        )
    else:
        resp = requests.get(
            url,
            params=request.GET,
            allow_redirects=False
        )
        content_type = resp.headers['content-type'].split(';')[0]

    # Data in KB
    statistics.data_sent += decimal.Decimal(len(request.body) / 1000)
    statistics.data_downloaded += decimal.Decimal(len(resp.content) / 1000)

    if resp.status_code == 302:
        statistics.save()
        new_location = resp.headers['location'].replace(site_obj.url, "/")
        if new_location == "/":
            return redirect(reverse(
                'site',
                kwargs={
                    'site_pk': site_pk,
                    'site_slug': site_slug,
                    'domain_url': new_location
                }
            ))
        return redirect(new_location)

    if content_type != "text/html":
        statistics.save()
        return HttpResponse(resp.content, content_type=content_type)

    soup = BeautifulSoup(resp.text, "lxml")

    services.change_tags_link(site_pk, site_slug, soup.find_all('link', href=True), 'href')
    services.change_tags_link(site_pk, site_slug, soup.find_all('meta', content=True), 'content')
    services.change_tags_link(site_pk, site_slug, soup.find_all('a', href=True), 'href')
    services.change_tags_link(site_pk, site_slug, soup.find_all('img', src=True), 'src')
    services.change_tags_link(site_pk, site_slug, soup.find_all('script', src=True), 'src')
    services.change_tags_link(site_pk, site_slug, soup.find_all('form', action=True), 'action')

    if resp.headers.get("Content-Length") != 0 and len(resp.content):
        statistics.page_transitions += 1
    statistics.save()

    return HttpResponse(str(soup), content_type=content_type)


@login_required(login_url='login')
def personal_cabinet(request):
    context = {
        'title': f'{request.user.username} Personal Cabinet',
        'sites': Site.objects.select_related("statistics").filter(user=request.user),
        'user_profile_form': UserProfileForm(instance=request.user.userprofile)
    }

    return render(request, "vpn_service/personal_cabinet.html", context)


@require_POST
@login_required(login_url='login')
def change_profile(request):
    profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
    if profile_form.is_valid():
        profile_form.save()

        messages.success(request, "Profile changed successfully")
    else:
        messages.error(request, profile_form.errors)
    return redirect('personal_cabinet')


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
