#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.conf.urls import url
from . import views
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    url(r'^addcargoods/(?P<did>\d*)$', views.AddCarGoods.as_view(), name='addcargoods'),  # 添加购物车
    url(r'^showcargoods/$', views.ShowCarGoods.as_view(), name='showcargoods'),  # 展示
    url(r'^delcargoods/(?P<gid>\d*)$', views.DelCarGoods.as_view(), name='delcargoods'),  # 删除
    url(r'^updatecargoods/(?P<gid>\d*)$', views.UpdateCarGoods.as_view(), name='updatecargoods'),  # 修改
]
