#!/usr/bin/python
# -*- coding:utf-8 -*-
import uuid

#中间件给用户设置cookie
class ShoppingGiveCookie(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.COOKIES.get('mysessionid'):
            response.set_cookie('mysessionid', str(uuid.uuid4()))
        return response
