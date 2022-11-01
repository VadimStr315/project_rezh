from email.policy import default
from django import forms
from personal_area.models import *

class Appeal_form(forms.Form):
    name = forms.CharField(max_length=255)
    surname = forms.CharField(max_length=255)
    patronymic = forms.CharField(max_length=255)
    city = forms.CharField(max_length=255, initial='Реж')
    street = forms.CharField(max_length=255)
    house = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    type_of_appeal= forms.CharField(max_length=255)
    theme = forms.CharField(max_length=255)
    category_of_benefits = forms.CharField(max_length=255)
    social_situation = forms.CharField(max_length=255)
    # deputy = forms.ModelChoiceField(queryset=Deputy.objects.all())
    deputy = forms.CharField(max_length=100)
    message = forms.CharField(max_length=1000)


class Search_form(forms.Form):
    number=forms.IntegerField(min_value=1000,max_value=9999)
    pin=forms.IntegerField(min_value=1000,max_value=9999)


class Search_appeals_form(forms.Form):
    number = forms.IntegerField()
    topic = forms.CharField(max_length=255)
    category = forms.CharField(max_length=255)
    start_time = forms.DateTimeField()
    end_time = forms.DateTimeField()