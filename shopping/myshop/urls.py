#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^register/$", views.Register.as_view(), name='register'),
    url(r"^check_username/$", views.CheckUsername.as_view(), name='check_username'),
    url(r"^active/$", views.AvtiveEmail.as_view(), name='active'),
    url(r"^login/$", views.Login.as_view(), name='login'),
    url(r"^logout/$", views.Logout.as_view(), name='logout'),
    url(r"^usercenterinfo/$", views.UserCenterInfo.as_view(), name='usercenterinfo'),
    url(r"^usercentersite/$", views.UserCenterSite.as_view(), name='usercentersite'),
    url(r"^usercentersetsite/$", views.UserCenterSetSite.as_view(), name='usercentersetsite'),
    url(r"^usercenterdelsite/$", views.UserCenterDelSite.as_view(), name='usercenterdelsite'),
    url(r"^usercenterorder/$", views.UserCenterOrder.as_view(), name='usercenterorder'),
]
