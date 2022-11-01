from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('news/', News.as_view(), name='news'),
    path('news/detail>', news_detail, name='news_detail'),
    path('about/', about, name='about'),
    path('vote/', vote, name='vote'),
    path('deputy_commission', deputy_commission, name='deputy_commission'),
    path('municipal_service', municipal_service, name='municipal_service'),
    path('appeals_info/', appeals_info, name='appeals_info'),
    path('appeal-<int:appeal_id>/', show_appeal_to_applicant, name='my_appeal'),
    path('appeal-<int:appeal_id>/detail', ShowDetailAppealToApplicant.as_view(), name='my_detail_appeal'),
]