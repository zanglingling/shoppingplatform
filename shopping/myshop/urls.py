#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^register/$", views.Register.as_view(), name='register'),  # 注册用户
    url(r"^check_username/$", views.CheckUsername.as_view(), name='check_username'),  # 注册用户验证
    url(r"^active/$", views.AvtiveEmail.as_view(), name='active'),  # 激活用户
    url(r"^login/$", views.Login.as_view(), name='login'),  # 登录用户
    url(r"^logout/$", views.Logout.as_view(), name='logout'),  # 注销用户
    url(r"^usercenterinfo/$", views.UserCenterInfo.as_view(), name='usercenterinfo'),  # 用户个人中心
    url(r"^usercentersite/$", views.UserCenterSite.as_view(), name='usercentersite'),  # 用户收货地址展示
    url(r"^usercentersetsite/$", views.UserCenterSetSite.as_view(), name='usercentersetsite'),  # 用户收货地址设置
    url(r"^usercenterdelsite/$", views.UserCenterDelSite.as_view(), name='usercenterdelsite'),  # 用户收货地址删除
    url(r"^usercenterorder/$", views.UserCenterOrder.as_view(), name='usercenterorder'),  # 用户订单展示
]
