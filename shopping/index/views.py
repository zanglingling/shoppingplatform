# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse
from django.views import View
# from django.contrib.auth.mixins import LoginRequiredMixin
from .models import GoodsInfo, GoodsArea, GoodsCategory
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from index.cache_record import GoodsBrowseCache
from django.db.models import F


class Index(View):
    def get(self, request):
        goods_list = []
        categorys = GoodsCategory.objects.filter(status=0)
        for i in categorys:
            goods_infos = GoodsInfo.objects.filter(category=i).order_by('click_count')[:4]
            goods_list.append({
                'category': i,
                'good_infos': goods_infos
            })
        return render(request, 'shop/index.html', {'goods_list':goods_list})


class CategorysGoodsInfo(View):
    def get(self, request, cid):
        order_by = request.GET.get('curr_order', 'id')

        goods_list = GoodsInfo.objects.filter(category=cid).order_by(order_by)
        try:
            page = int(request.GET.get('page', 1))
        except PageNotAnInteger:
            page = 1
        # 为完成查询字符串生成提供请求对象的分页
        # 需要在中间传入一个数字,这个数字表示每页显示几个
        paginator = Paginator(goods_list, 10, request=request)

        goods = paginator.page(page)

        return render(request, 'shop/list.html', locals())


class Detail(View):
    def get(self, request, did):
        good = GoodsInfo.objects.filter(id=did).first()
        # 添加一个浏览记录， 如果登录，则以用户保存
        # 如果未登录，则保存对应IP

        goodbrowsecache = GoodsBrowseCache()
        if request.user.is_authenticated:
            goodbrowsecache.add_browse(request.user.id, did)
        else:
            if request.META.get('HTTP_X_FORWARDED_FOR'):
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            goodbrowsecache.add_browse(ip, did)
            print(ip)
        GoodsInfo.objects.filter(id=did).update(click_count=F('click_count') + 1)
        return render(request, 'shop/detail.html', locals())
