from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from .models import Site, UserProfile

User = get_user_model()


class RegisterUser(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'form-control'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'form-control'}))


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']

    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))


class CreateSite(forms.ModelForm):
    class Meta:
        model = Site
        fields = ["name", "url"]

    def __init__(self, *args, **kwargs):
        super(CreateSite, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'name'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['url'].widget = forms.URLInput(attrs={'placeholder': 'url', 'class': 'form-control'})


class LoginUser(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginUser, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['required'] = True
        self.fields['password'].widget.attrs['placeholder'] = 'password'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['required'] = True
