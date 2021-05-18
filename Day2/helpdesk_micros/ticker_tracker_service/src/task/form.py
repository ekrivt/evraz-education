from django import forms
from django.db import models
from django.contrib.auth import get_user_model
from django.http.response import HttpResponse
from http import HTTPStatus
import requests

from .models import Task

from project.views import Project

User = get_user_model()

OPEN = 'open'
RESOLVE = 'resolve'
CANCEL = 'cancel'

STATUS_CHOICES = (
    (OPEN, 'Открыт'),
    (RESOLVE, 'Решен'),
    (CANCEL, 'Отменен')
)

class TaskListForm(forms.ModelForm):

    project_list = Project.objects.all()
    users_list = User.objects.all()
    
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Task
        fields = ['name', 'project', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Название'
        self.fields['project'].label = 'Проект'
        self.fields['status'].label = 'Статус'

    def clean_name(self):
        name = self.cleaned_data['name']
        if Task.objects.filter(name=name).exists():
            raise forms.ValidationError(
                'Название занято'
            )
        return name
    
class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        post_data = {
                        "username": username,
                        "password": password
                    }
        response = requests.post('http://user-service:8000/login/' , json=post_data, headers={ "Content-Type": "application/json" })

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise forms.ValidationError('Пользователь с логином {} не найден в системе'.format(username))
        if response.status_code == HTTPStatus.BAD_REQUEST:
            raise forms.ValidationError("Неверный пароль")

        return self.cleaned_data


class RegistrationForm(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    status = forms.CharField(max_length=10) #choices=STATUS_CHOICES, default=CLIENT, verbose_name='Статус')
    #email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердите пароль'
        self.fields['status'].lable = 'Статус'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        post_data = {
            "username": username,
            "password": password
        }
        response = requests.post('http://user-service:8000/registration/' , json=post_data, headers={ "Content-Type": "application/json" })

        if response.status_code == HTTPStatus.CONFLICT:
            raise forms.ValidationError("Имя занято")
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
            
        return self.cleaned_data
