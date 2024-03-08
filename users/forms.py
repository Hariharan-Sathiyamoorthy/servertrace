from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core import validators

class UserSignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"placeholder": "username"}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',"placeholder": "Password"}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',"placeholder": "Retype Password"}) ,required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control',"placeholder": "email"}) ,required=True)
    
    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']
    
class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"placeholder": "username"}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',"placeholder": "Password"}), required=True)

    class Meta:
        model = User
        fields = ['username', 'password']

class UserEditForm(forms.ModelForm):
    is_admin = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),required=False)
    is_techie = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),required=False)

    class Meta:
        model = User
        fields = ['is_admin','is_techie']