# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


# 建立用户信息表
class UserInfo(AbstractUser):
    GENDER = (
        (0, '男'), (1, '女')
    )
    gender = models.SmallIntegerField(u'性别', choices=GENDER, default=0)
    receiver = models.ForeignKey('ReceiverUser', null=True, blank=True, default=None)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailRecord(models.Model):
    email_type = models.SmallIntegerField(verbose_name='邮件类型', choices=((0, '激活'), (1, '重置密码')))
    user = models.ForeignKey(UserInfo, verbose_name='用户')
    code = models.CharField(verbose_name='验证码', max_length=40)
    create_email = models.DateTimeField(auto_now=True, verbose_name='发送时间')

    class Meta:
        verbose_name = '邮箱记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user


class ReceiverUser(models.Model):
    receivername = models.CharField(verbose_name='收货人', max_length=50)
    receivercity = models.CharField(verbose_name='城市', max_length=30)
    receivertelephone = models.CharField(verbose_name='联系电话', max_length=11)
    receiveradress = models.CharField(verbose_name='收货地址', max_length=300)
    receiveruser = models.ForeignKey('UserInfo')

    class Meta:
        verbose_name = '收货信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.receivername
