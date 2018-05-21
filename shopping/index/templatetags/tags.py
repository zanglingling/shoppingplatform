#!/usr/bin/python
# -*- coding:utf-8 -*-

from django import template
from index.models import GoodsCategory, GoodsInfo
from django.conf import settings
from django.shortcuts import reverse
from django.utils.safestring import mark_safe
import urllib

register = template.Library()


@register.inclusion_tag('shop/refferral_good.html')
def new_goods(cid=None):
    if cid:
        goods = GoodsInfo.objects.filter(category=cid).order_by('-id')[:3]
    else:
        goods = GoodsInfo.objects.order_by('-id')[:3]
    return {
        'goods': goods,
        'url': settings.MEDIA_URL
    }


# @register.simple_tag
# def smart_page(curr_page, page_obj, url_name, request_url, page_name="curr_page", args=[], kwargs={}):
#     # 第一步，完成基本分页
#     # 第二步，添加有参数的分页
#     # 第三步，锁定固定长度的分页
#     page_str = '<div class="pagenation">'
#     url = reverse(url_name, args=args, kwargs=kwargs)
#     p = page_obj.page(curr_page)
#     max_page_count = 5
#     page_name = page_name.encode("utf8")
#
#     # 截取当前url的get参数，赋值到当前的url中
#     params = {}
#     request_url = urllib.unquote(request_url.encode("utf8"))
#     if len(request_url.split("?")) >= 2:
#         for param in request_url.split("?")[-1].split("&"):
#             params[param.split("=")[0]] = param.split("=")[1]
#
#     # 锁定固定长度
#     # 1、获取当前所有的分页码
#     # 2、获取当前页码的左右偏移量
#     # 例：
#     #   当前分页码为 [1,2,3,4,5,6,7,8,9]
#     #   设置当前需要展示5个页面， 当前页面5
#     #   每边的偏移量为2
#     #   先获取左右的偏移量，得到分页码为[3,4,5,6,7,8,9]
#     #   迭代当前分页码，如果超过最大页码数，则退出
#
#     # 获取当前分页码
#     page_range = [cp for cp in page_obj.page_range]
#
#     # 获取当前偏移量
#     center_index = max_page_count / 2
#     # 计算当前偏移位置
#     page_index = page_range.index(curr_page)
#     if page_index > center_index:
#         _page_range = page_range[page_index - center_index:]
    #
    #     # 如果当前偏移位置不足，则补充偏移量
    #     if len(_page_range) < max_page_count:
    #         index = max_page_count - len(_page_range)
    #         print(page_index - center_index) - index
    #
    #         page_range = page_range[(page_index - center_index) - index:]
    #     else:
    #         page_range = _page_range
    #
    # # 获取上一页
    # if p.has_previous():
    #     params[page_name] = curr_page - 1
    #     curl_url = "%s?%s" % (url, urllib.urlencode(params))
    #     page_str += u'<a href="%s">上一页</a>' % curl_url
    #
    # # 获取当前中间页码
    # for i, cp in enumerate(page_range):
    #     params[page_name] = cp
    #     curl_url = u"%s?%s" % (url, urllib.urlencode(params))
    #     if cp == curr_page:
    #         page_str += u'<a href="%s" class="active">%s</a>' % (curl_url, cp)
    #     else:
    #         page_str += u'<a href="%s">%s</a>' % (curl_url, cp)
    #
    #     # 如超过最大页码，则退出，保证只显示设置的最大页码数
    #     if i + 1 >= max_page_count:
    #         break
    #
    # # 获取下一页
    # if p.has_next():
    #     params[page_name] = curr_page + 1
    #     curl_url = "%s?%s" % (url, urllib.urlencode(params))
    #     page_str += u'<a href="%s">下一页</a>' % curl_url

    # page_str += "<input type='text'/><a herf='#' >go</a>"
    # page_str += "</div>"
    # 渲染成html标签
    # return mark_safe(page_str)
