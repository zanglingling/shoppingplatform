# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import UserInfo, ReceiverUser


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['username', 'receiver', 'email']
    list_filter = ['username', 'receiver', 'email']
    list_per_page = 10
    search_fields = ['username', 'receiver', 'email']


@admin.register(ReceiverUser)
class ReceiverUserAdmin(admin.ModelAdmin):
    list_display = ['receivername', 'receivercity', 'receivertelephone']
    list_filter = ['receivername', 'receivercity', 'receivertelephone']
    list_per_page = 10
    search_fields = ['receivername', 'receivercity', 'receivertelephone']
