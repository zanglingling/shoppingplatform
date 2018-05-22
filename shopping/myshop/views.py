#!/usr/bin/python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.views import View
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout

from .models import UserInfo, EmailRecord, ReceiverUser
from .forms import UserInfoForm, LoginForm, ReceiverUserForm
from utils.register_email import register_email
from index.models import GoodsInfo
from index.cache_record import GoodsBrowseCache
from shop_order.models import OrderMain

from pure_pagination import Paginator, PageNotAnInteger


# 注册用户
class Register(View):
    def get(self, request):
        return render(request, 'account/register.html')

    def post(self, request):
        register_form = UserInfoForm(request.POST)  # 获取表单信息
        if register_form.is_valid():  # 验证表单
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            email = register_form.cleaned_data['email']
            user = UserInfo()
            user.username = username
            user.password = make_password(password1)
            user.email = email
            user.is_active = False  # 激活字段False
            user.save()
            register_email(user)  # 发送邮件
            return render(request, 'account/send_success.html')
        else:
            return render(request, 'account/register.html', locals())


# ajxs用户注册
class CheckUsername(View):
    def get(self, request):
        username = request.GET.get("username")
        count = UserInfo.objects.filter(username=username).count()
        return JsonResponse({"count": count})


# 邮箱激活
class AvtiveEmail(View):
    def get(self, request):
        code = request.GET.get('code')
        email = EmailRecord.objects.filter(code=code).first()
        email.user.is_active = True
        email.user.save()
        return redirect(reverse('account:login'))


# 登录用户
class Login(View):
    def get(self, request):
        return render(request, 'account/login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            # 如果验证成功就会返回一个用户，否则就返回空
            user = authenticate(username=username, password=password)  # 验证用户名，密码
            if user:
                login(request, user)
                return redirect(reverse('index:index'))
            else:
                return render(request, 'account/login.html', {'error': '用户或者密码错误'})
        else:
            return render(request, 'account/login.html', locals())


# 注销
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('index:index'))


# 用户中心展示
class UserCenterInfo(LoginRequiredMixin, View):
    # login_url = '/account/login/'
    def get(self, request):
        ids = GoodsBrowseCache().lrange_record(request.user.id)  # 根据用户id查询浏览记录
        ids = list(ids)
        ls = []
        for i in ids:
            if i not in ls:
                ls.append(i)
        view_record = GoodsInfo.objects.filter(id__in=ls[:3]).all()
        return render(request, 'account/user_center_info.html', locals())


# 用户地址展示
class UserCenterSite(LoginRequiredMixin, View):
    def get(self, request):
        receiver_infos = ReceiverUser.objects.all()
        return render(request, 'account/user_center_site.html', locals())

    def post(self, request):  # ajxs地址信息提交
        receiver_form = ReceiverUserForm(request.POST)
        if receiver_form.is_valid():
            receiver = ReceiverUser()
            receiver.receivername = receiver_form.cleaned_data['name']
            receiver.receivercity = receiver_form.cleaned_data['city']
            receiver.receivertelephone = receiver_form.cleaned_data['telephone']
            receiver.receiveradress = receiver_form.cleaned_data['address']
            receiver.receiveruser = request.user
            receiver.save()
            return JsonResponse({'status': 0})
        else:
            return JsonResponse({'status': 1, 'error': receiver_form.errors})


# 收货地址设置
class UserCenterSetSite(View):
    def get(self, request):
        data_id = request.GET.get('data_id')
        request.user.receiver_id = data_id
        request.user.save()
        return JsonResponse({'status': 0,
                             'receivername': request.user.receiver.receivername,
                             'receivercity': request.user.receiver.receivercity,
                             'receivertelephone': request.user.receiver.receivertelephone,
                             'receiveradress': request.user.receiver.receiveradress,
                             })


# 收货地址删除
class UserCenterDelSite(View):
    def get(self, request):
        data_id = int(request.GET.get('data_id'))
        is_default = 0
        if request.user.receiver_id == data_id:  # 删除的地址等于默认地址
            request.user.receiver_id = None
            request.user.save()
            is_default = 1
        ReceiverUser.objects.filter(id=data_id).delete()
        return JsonResponse({'status': 0, 'is_default': is_default})


# 用户订单展示
class UserCenterOrder(LoginRequiredMixin, View):
    def get(self, request):
        ordermain = OrderMain.objects.filter(user=request.user)  # 获取订单
        try:
            current_page = int(request.GET.get('page', 1))
        except PageNotAnInteger:
            current_page = 1
        paginator = Paginator(ordermain, 3, request=request)
        orders = paginator.page(current_page)
        return render(request, 'account/user_center_order.html', locals())
