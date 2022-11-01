from django import forms
from django.contrib.auth.forms import AuthenticationForm
from personal_area.models import *


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white',
            'id': 'name-b766',
            'placeholder': 'Введите Ваш Логин',
            'name': 'name',
            'required': '',
            #'type': 'text'
        }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white',
            'id': 'email-b766',
            'placeholder': 'Введите Ваш Пароль',
            'name': 'email',
            'required': '',
            #'type': 'email'
        }))


class FindAppealsForm(forms.Form):
    deputy = forms.ModelChoiceField(required=False, empty_label='Все', queryset=Deputy.objects.all(), widget=forms.Select(attrs={
        'id': 'deputy',
        'name': 'deputy',
        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white'
    }))
    topic = forms.ModelChoiceField(required=False, empty_label='Все', queryset=Topic.objects.all(), widget=forms.Select(attrs={
        'id': 'topic',
        'name': 'topic',
        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white'
    }))
    category = forms.ModelChoiceField(required=False, empty_label='Все', queryset=AppealCategory.objects.all(), widget=forms.Select(attrs={
        'id': 'category',
        'name': 'category',
        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white'
    }))
    start_time = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={
        'type': 'date',
        'id': 'start_time',
        'name': 'start_time',
        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white'
    }))
    end_time = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={
        'type': 'date',
        'id': 'end_time',
        'name': 'end_time',
        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white'
    }))