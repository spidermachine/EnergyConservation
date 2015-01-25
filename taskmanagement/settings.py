# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
"""
Django settings for taskmanagement project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0+qil77ex*lz7&$m%4za$x4s_d80%t(*l&j^e-+g8+mjsva7&p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'djcelery',
    'admintasks',
    'web',
    'finance',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'taskmanagement.urls'

WSGI_APPLICATION = 'taskmanagement.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'finance',
        'USER': 'finance',
        'PASSWORD': 'finance',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')



# celery
BROKER_URL = 'redis://localhost:6379/0'

# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

CELERY_RESULT_BACKEND = 'db+mysql://finance:finance@localhost:3306/finance'

CELERY_ALWAYS_EAGER = True

CELERY_ENABLE_UTC = False

from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    # Executes every Monday morning at 7:30 A.M
    u'采集基金持股': {
        'task': 'admintasks.tasks.fund_share_task',
        'schedule': crontab(minute='*/3', hour='*', day_of_week='*'),
        'args': (),
        'kwargs': {"timeout": 10, "show": True, "wait": True}
    },
    u'采集基金评级': {
        'task': 'admintasks.tasks.fund_grade_task',
        'schedule': crontab(minute='0', hour=21, day_of_week='*'),
        'args': (),
        'kwargs': {"url": "http://cn.morningstar.com/quickrank/default.aspx",
                   "timeout": 600,
                   "continue": True,
                   "text": "&gt;",
                   "tag": "a",
                   "id": "ctl00_cphMain_gridResult",
                   "wait": True
        }
    },
    u'采集基金列表': {
        'task': 'admintasks.tasks.fund_list_task',
        'schedule': crontab(minute='0', hour=17, day_of_week='*'),
        'args': (),
        'kwargs': {"url": "http://quotes.money.163.com",
                   "timeout": 20,
                   "continue": True,
                   "class": "dbtable",
                   "tag": "a",
                   "text": "下一页",
                   "query": "'#FN'",
                   "sub_domain": "股票型",
                   "header_text": "基金净值"
        }
    },
    u'采集行业资金流': {
        'task': 'admintasks.tasks.industry_task',
        'schedule': crontab(minute=0, hour=19, day_of_week='*'),
        'args': (),
        'kwargs': {"url": "http://data.10jqka.com.cn/funds/hyzjl",
                   "continue": True,
                   "class": "m_table",
                   "timeout": 600,
                   "text": u"下一页",
                   "tag": "a",
                   "wait": True
        }
    },u'采集股票评级': {
        'task': 'admintasks.tasks.stock_grade_task',
        'schedule': crontab(minute=0, hour=22, day_of_week='*'),
        'args': (),
        'kwargs': {
            "url":"http://vip.stock.finance.sina.com.cn/q/go.php/vIR_SumRating/index.phtml",
            "timeout": 600,
            "tag": "a",
            "text": u"下一页",
            "class": "list_table",
            "continue": True,
            "show": True,
            "wait": True
        }
    },
    u'采集股票分类列表': {
        'task': 'admintasks.tasks.stock_task',
        'schedule': crontab(minute=0, hour=20, day_of_week='*'),
        'args': (),
        'kwargs': {
            "url": "http://quotes.money.163.com/",
            "continue": True,
            "tag": "a",
            "text": "下一页",
            "more_text": "更多",
            "timeout": 10,
            "query": "#query:hy",
            "class": "stocks-info-table",
            "wait": True
        }
    }
    # ,
    # u'易精灵': {
    #     'task': 'admintasks.tasks.yjl_task',
    #     'schedule': crontab(minute=0, hour=23, day_of_week='*'),
    #     'args': (),
    #     'kwargs': {"timeout": 10, "show": True, "wait": True}
    # }
}

import djcelery

djcelery.setup_loader()

