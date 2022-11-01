from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', AppealHome.as_view(), name='personal_area'),
    path('logout', logout_user, name='logout'),
    path('appeals/<int:appeal_id>', show_appeal_to_deputy, name='appeal'),
    path('analytic', analytic_detail, name='analytic'),
    path('appeals/<int:appeal_id>/detail', ShowDetailAppeal.as_view(), name='detail_appeal')
]
