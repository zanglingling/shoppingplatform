#!/usr/bin/python
# -*- coding:utf-8 -*-
from django_redis import get_redis_connection


class BaseRedis(object):
    def __init__(self):
        self.conn = get_redis_connection('default')