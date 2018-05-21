#!/usr/bin/python
# -*- coding:utf-8 -*-
from utils.cachebase import BaseRedis


class ShoppingCarCache(BaseRedis):
    key = "shop_cart_key_{0}"

    def add_car(self, session_id, gid, buy_num):
        num = self.conn.hget(self.key.format(session_id), gid)
        if num:
            num = int(num)
        else:
            num = 0
        buy_num = buy_num + num
        self.conn.hset(self.key.format(session_id), gid, buy_num)

    def hlen(self, session_id):
        return self.conn.hlen(self.key.format(session_id))

    def hgetall(self, session_id):
        return self.conn.hgetall(self.key.format(session_id))

    def hdel(self, session_id, gid):
        self.conn.hdel(self.key.format(session_id), gid)

    def hupdate(self, session_id, gid, buy_num):
        self.conn.hset(self.key.format(session_id), gid, buy_num)
