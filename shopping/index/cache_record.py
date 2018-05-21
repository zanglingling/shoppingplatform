#!/usr/bin/python
# -*- coding:utf-8 -*-

from utils.cachebase import BaseRedis

class GoodsBrowseCache(BaseRedis):
    key = 'user_browse_{0}'

    def add_browse(self, key_value, gid):
        self.conn.lpush(self.key.format(key_value), gid)

    def lrange_record(self, user_id):
        return self.conn.lrange(self.key.format(user_id), 0, 100)
