#!/usr/bin/python
# -*- coding:utf-8 -*-
from django import forms
from .models import UserInfo


# 用户注册表单验证
class UserInfoForm(forms.Form):
    username = forms.CharField(required=True, max_length=20, min_length=5)
    password1 = forms.CharField(required=True, max_length=20, min_length=8)
    password2 = forms.CharField(required=True, max_length=20, min_length=8)
    email = forms.EmailField(required=True)
    allow = forms.CharField(required=True)

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('两次密码不一样')
        return password2

    def clean_username(self):
        username = self.cleaned_data["username"]
        if UserInfo.objects.filter(username=username).first():
            raise forms.ValidationError('用户已存在')
        return username


# 用户登录表单验证
class LoginForm(forms.Form):
    username = forms.CharField(min_length=5, max_length=20)
    password = forms.CharField(min_length=8, max_length=20)


# 用户收货地址表单验证
class ReceiverUserForm(forms.Form):
    name = forms.CharField(min_length=2, max_length=50, required=True)
    city = forms.CharField(min_length=2, max_length=30, required=True)
    telephone = forms.CharField(min_length=11, max_length=11, required=True)
    address = forms.CharField(min_length=2, max_length=300, required=True)
