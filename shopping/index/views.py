# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from .models import GoodsInfo, GoodsCategory
from pure_pagination import Paginator, PageNotAnInteger
from index.cache_record import GoodsBrowseCache
from django.db.models import F


# 首页展示
class Index(View):
    def get(self, request):
        goods_list = []
        categorys = GoodsCategory.objects.filter(status=0)  # 类别查询
        for i in categorys:
            goods_infos = GoodsInfo.objects.filter(category=i).order_by('click_count')[:4]  # 对每一类取前4个
            goods_list.append({
                'category': i,
                'good_infos': goods_infos
            })
        return render(request, 'shop/index.html', {'goods_list': goods_list})


# 分类展示
class CategorysGoodsInfo(View):
    def get(self, request, cid):
        order_by = request.GET.get('curr_order', 'id')  # 获取类别id

        goods_list = GoodsInfo.objects.filter(category=cid).order_by(order_by)  # 根据类别查询商品
        # 分页
        try:
            page = int(request.GET.get('page', 1))
        except PageNotAnInteger:
            page = 1
        # 为完成查询字符串生成提供请求对象的分页
        # 需要在中间传入一个数字,这个数字表示每页显示几个
        paginator = Paginator(goods_list, 10, request=request)
        goods = paginator.page(page)
        return render(request, 'shop/list.html', locals())


# 商品细节展示
class Detail(View):
    def get(self, request, did):
        good = GoodsInfo.objects.filter(id=did).first()  # 获取商品id
        # 添加一个浏览记录， 如果登录，则以用户保存
        # 如果未登录，则保存对应IP

        goodbrowsecache = GoodsBrowseCache()
        if request.user.is_authenticated:
            goodbrowsecache.add_browse(request.user.id, did)  # 购物车添加记录
        else:
            if request.META.get('HTTP_X_FORWARDED_FOR'):
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            goodbrowsecache.add_browse(ip, did)  # 未登录情况，根据ip添加购物记录
            print(ip)
        GoodsInfo.objects.filter(id=did).update(click_count=F('click_count') + 1)  # 页面点击量
        return render(request, 'shop/detail.html', locals())
