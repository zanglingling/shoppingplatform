#!/usr/bin/python
# -*- coding:utf-8 -*-
from .cache import ShoppingCarCache
from .models import ShoppingCar


# 上下文对用户在登录和没登录情况下购物车商品数量的获取
def goods_num(request):
    mysessionid = request.COOKIES.get('mysessionid')
    shopcarcache = ShoppingCarCache()
    if request.user.is_authenticated():
        data = shopcarcache.hgetall(mysessionid)
        if data:
            for gid, buy_num in data.items():  # 合并未登录情况下的购物车记录
                shopcar, is_create = ShoppingCar.objects.update_or_create(user=request.user, goods_id=gid)
                shopcar.buy_num += int(buy_num)
                shopcar.save()
                shopcarcache.hdel(mysessionid, gid)

        goods_num = ShoppingCar.objects.filter(user=request.user).count()
    else:
        # 未登录从redis中获取当前购物车数量
        goods_num = shopcarcache.hlen(mysessionid)
    return {'goods_num': goods_num}
