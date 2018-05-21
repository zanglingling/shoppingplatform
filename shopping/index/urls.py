#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.conf.urls import url
from . import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    url(r"index/$", views.Index.as_view(), name='index'),
    url(r"categorys/(?P<cid>\d*)/$", views.CategorysGoodsInfo.as_view(), name='categorys'),
    url(r"detail/(?P<did>\d*)/$", views.Detail.as_view(), name='detail'),
]
