#!/usr/bin/python
# -*- coding:utf-8 -*-
from .models import GoodsCategory


def cacategorys_display(request):
    categorys = GoodsCategory.objects.filter(status=0)
    return {'categorys': categorys}
