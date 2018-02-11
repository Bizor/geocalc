from django.forms import ModelForm
from django.forms import widgets
from django.forms.widgets import *
from geobase.models import *
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import (
    authenticate, get_user_model, password_validation)

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин', 'value': '', 'autocomplete': 'off'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль', 'autocomplete': 'off'}),    
        }

class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ['project_name', 'project_points']
		widgets = {
			'project_name': forms.TextInput(attrs={'placeholder': 'Название проекта', 'autocomplete': 'off', 'required': 'Введите координату X'}),		
		}