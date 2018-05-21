#!/usr/bin/python
# -*- coding:utf-8 -*-
from myshop.models import EmailRecord
from django.conf import settings
from django.core.mail import send_mail
import uuid


def register_email(user):
    email = EmailRecord()
    email.email_type = 0
    email.user = user
    email.code = uuid.uuid4()  # 这里只要是一个唯一的加密的字符串即可
    email.save()
    email_title = '用户注册'
    url = "http://192.168.1.100:8000/account/active/?code=%s" % email.code
    html_message = u"<a href='%s'>欢迎注册，请点击该链接激活用户</a>" % url
    send_mail(email_title, "157", settings.EMAIL_FROM, [user.email], html_message=html_message)
