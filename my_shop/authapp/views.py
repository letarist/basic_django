import pytz
from django.shortcuts import render
from django.contrib import auth
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileEditForm
from authapp.models import ShopUser
from authapp.services import send_verify_email


def login(request):
    login_form = ShopUserLoginForm(data=request.POST)
    next_param = request.GET.get('next', '')
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            return HttpResponseRedirect(reverse('index'))
    context = {
        'login_form': login_form,
        'next_param': next_param
    }

    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            new_user = register_form.save()
            send_verify_email(new_user)
            return HttpResponseRedirect(reverse('index'))
    else:
        register_form = ShopUserRegisterForm()
    context = {
        'register_form': register_form
    }
    return render(request, 'authapp/register.html', context)


def edit(request):
    if request.method == 'POST':
        user_edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        user_profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        if user_edit_form.is_valid() and user_profile_form.is_valid():
            user_edit_form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        user_edit_form = ShopUserEditForm(instance=request.user)
        user_profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)

    context = {
        'user_edit_form': user_edit_form,
        'user_profile_form': user_profile_form,
    }
    return render(request, 'authapp/edit.html', context)


def verify(request, email, key):
    user = ShopUser.objects.filter(email=email).first()
    if user:
        if user.activate_key == key and user.is_activate_key_expired():
            user.activate()
            auth.login(request, user)
    return render(request, 'authapp/register_result.html')
