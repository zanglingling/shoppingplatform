#!/usr/bin/python
# -*- coding:utf-8 -*-
from utils.cachebase import BaseRedis


# 购物车redis缓存操作
class ShoppingCarCache(BaseRedis):
    key = "shop_cart_key_{0}"

    def add_car(self, session_id, gid, buy_num):  # redis添加记录
        num = self.conn.hget(self.key.format(session_id), gid)
        if num:
            num = int(num)
        else:
            num = 0
        buy_num = buy_num + num
        self.conn.hset(self.key.format(session_id), gid, buy_num)

    def hlen(self, session_id):  # redis获取记录长度
        return self.conn.hlen(self.key.format(session_id))

    def hgetall(self, session_id):  # 获取redis数据
        return self.conn.hgetall(self.key.format(session_id))

    def hdel(self, session_id, gid):  # 删除redis数据
        self.conn.hdel(self.key.format(session_id), gid)

    def hupdate(self, session_id, gid, buy_num):  # 修改数据
        self.conn.hset(self.key.format(session_id), gid, buy_num)
