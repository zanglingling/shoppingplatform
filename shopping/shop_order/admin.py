from django.contrib import admin
from .models import OrderDetail, OrderMain


@admin.register(OrderMain)
class OrderMainAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'order_statue', 'user', 'total', 'is_pay', 'receiver']
    list_filter = ['uuid', 'user', 'total', 'is_pay', 'receiver']
    list_per_page = 10
    search_fields = ['uuid', 'order_statue', 'user', 'total', 'is_pay', 'receiver']


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['order', 'goods_info', 'goods_price', 'goods_total', 'count']
    list_filter = ['order', 'goods_info', 'goods_price', 'goods_total', 'count']
    list_per_page = 10
    search_fields = ['order', 'goods_info', 'goods_price', 'goods_total', 'count']
