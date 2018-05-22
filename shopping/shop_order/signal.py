#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.dispatch import receiver
from .models import OrderMain, OrderDetail
from django.db.models.signals import pre_save
from django.db.models import F
from django.db import transaction


# 触发器，在订单详情保存时触发
@receiver(pre_save, sender=OrderMain)
def order_singoal(sender, **kwargs):
    order = kwargs['instance']
    if order.is_pay == '-1':
        details = OrderDetail.objects.filter(order=order)
        with transaction.atomic():
            for i in details:
                i.goods_info.stock = F('stock') + i.count
                i.goods_info.save()
