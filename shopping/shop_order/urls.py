#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^shoporder/(?P<oid>\d*)/$', views.ShowOrder.as_view(), name='shoporder'),  # 提交订单展示
    url(r'^cancelorder/$', views.CancelOrder.as_view(), name='cancelorder'),  # 取消订单
]
