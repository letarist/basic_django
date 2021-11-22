import hashlib

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.conf import settings
from django.forms import HiddenInput, forms
from authapp.models import ShopUser, ShopUserProfile
from django import forms
from datetime import datetime

import pytz


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError('Слишком мелкий')
        return data


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'avatar', 'email', 'age', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.is_active = False
        user.activate_key = hashlib.sha1(user.email.encode('utf-8')).hexdigest()[:6]
        user.activate_key_expired = datetime.now(pytz.timezone(settings.TIME_ZONE))
        user.save()
        return user


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'avatar', 'email', 'age', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.widgets.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

            if field_name == 'password':
                field.widget = HiddenInput()

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError('Слишком мелкий')
        return data


class ShopUserProfileEditForm(forms.ModelForm):
    class Meta:
        model = ShopUserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
