# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import GoodsInfo, GoodsCategory, GoodsArea


class GoodsCategoryInline(admin.StackedInline):
    model = GoodsInfo
    extra = 1


@admin.register(GoodsCategory)
class GoodsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'status']
    list_filter = ['name', 'status']
    list_per_page = 10
    search_fields = ['name', 'status']
    inlines = [GoodsCategoryInline]


class GoodsAreaInline(admin.StackedInline):
    model = GoodsInfo
    extra = 1


@admin.register(GoodsArea)
class GoodsAreaAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    list_per_page = 10
    search_fields = ['name']
    inlines = [GoodsCategoryInline]


@admin.register(GoodsInfo)
class GoodsInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'status', 'stock']
    list_filter = ['name', 'stock', 'description', 'category', 'area']
    list_per_page = 10
    search_fields = ['name', 'stock', 'description', 'category', 'area']
