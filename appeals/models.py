from django.db import models

# from django import forms

# class Appeal_form((models.Model)):
#     name = models.CharField(max_length=255)
#     surname = models.CharField(max_length=255)
#     patronymic = models.CharField(max_length=255)
#     city = models.CharField(max_length=255)
#     street = models.CharField(max_length=255)
#     house = models.CharField(max_length=255)
#     phone = models.CharField(max_length=255)
#     email = models.EmailField(max_length=255)
#     type_of_appeal= models.CharField(max_length=255)
#     theme = models.CharField(max_length=255)
#     category_of_benefits = models.CharField(max_length=255)
#     social_situation = models.CharField(max_length=255)
#     deputy = models.CharField(max_length=100)
#     message = models.CharField(max_length=1000)
#     date_of_ordering = models.CharField(max_length=10)

# class Form_for_Appeal (forms.ModelForm):
#     class Meta:
#         model= Appeal_form
#         exclude =['date_of_ordering']