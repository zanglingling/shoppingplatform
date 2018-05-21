from django.db import models
from index.models import GoodsInfo
from myshop.models import UserInfo


# 购物车模型
class ShoppingCar(models.Model):
    user = models.ForeignKey(UserInfo, verbose_name='用户')
    goods = models.ForeignKey(GoodsInfo, verbose_name='商品')
    buy_num = models.IntegerField(verbose_name='购买数', default=0)
    create_time = models.DateTimeField(verbose_name='添加时间', auto_now=True)

    class Meta:
        unique_together = ('user', 'goods')  # 唯一约束
