from django.contrib import admin
from django.urls import path, include
from .views import success, send_appeal, review_appeals, review_appeal_peoples, redirect_form

urlpatterns = [
    path('',send_appeal, name='appeals_form'),
    path('success',success,name='success'),
    path('review_appeal_peoples', review_appeal_peoples, name='review_appeal_peoples'),
    path('redirect_form-<int:appeal_id>/', redirect_form, name='redirect_form'),
    path('review_appeals-<int:appeal_id>/', review_appeals, name='review_appeals'),
    path('search',success,name='success'),
]
