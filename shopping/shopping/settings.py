# -*- coding: utf-8 -*-
"""
Django settings for shopping project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7tplub7xn($8r&m7ytm%g*j)xm+9c-bt&l5*euy2b!p%0+**8c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myshop.apps.MyshopConfig',
    'index',
    'tinymce',
    'pure_pagination',
    'shopping_car',
    'shop_order',
    'haystack',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'shopping_car.middleware.ShoppingGiveCookie'
]

ROOT_URLCONF = 'shopping.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                'index.context_processors.cacategorys_display',
                'shopping_car.context_processors.goods_num'
            ],
        },
    },
]

WSGI_APPLICATION = 'shopping.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 引擎
        'NAME': 'shopping',  # 库名
        'USER': 'wangjun',  # 用户名
        'PASSWORD': 'qwe123',  # 密码
        'HOST': '127.0.0.1',  # 地址
        'PORT': '3306',  # 端口
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# login_url = '/account/login/'
LOGIN_URL = '/account/login/'

# 配置媒体路径
MEDIA_URL = '/static/images/'
MEDIA_ROOT = (
    os.path.join(BASE_DIR, 'static/images')
)

AUTH_USER_MODEL = 'myshop.UserInfo'

# 邮件引擎
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# smtp邮箱的host地址，每个邮箱都是不同的
EMAIL_HOST = 'smtp.163.com'
# smtp邮箱的端口
EMAIL_PORT = 25
# 发送邮件的邮箱（发件人）
EMAIL_HOST_USER = '15705107305@163.com'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = '19930510wj'
# 收件人看到的发件人
EMAIL_FROM = 'store <15705107305@163.com>'  # 需要和邮箱号码一致

TINYMCE_JS_URL = "/static/tiny_mce/tiny_mce.js"
TINYMCE_JS_ROOT = "/static/tiny_mce/"
TINYMCE_DEFAULT_CONFIG = {
    "height": 600,
    "width": 400,
    'theme': "advanced",
    'plugins': "table,spellchecker,paste,searchreplace",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
}
TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True

PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 10,  # 这个是显示中间有多少个按键
    'MARGIN_PAGES_DISPLAYED': 2,  # 是将显示的第一页和最后一页相邻的页数（默认值为2）

    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}

# django-redis配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",  # redis的ip地址
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",  # 使用redis默认的缓存
        }
    }
}
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'utils.whoosh_zh_index.WhooshEngine',  # 默认引擎为英文搜索引擎，改为中文
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}
# HAYSTACK_SEARCH_RESULTS_PER_PAGE = 2  # 做分页显示用
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'  # 当添加、修改、删除数据时，自动生成索引


STATIC_ROOT = "collectstatic"