#!/usr/bin/python
# -*- coding:utf-8 -*-
from .models import GoodsCategory


# 上下文关于商品类别
def cacategorys_display(request):
    categorys = GoodsCategory.objects.filter(status=0)
    return {'categorys': categorys}
