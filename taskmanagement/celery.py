# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
from __future__ import absolute_import
__author__ = 'keping.chu'


import os

from celery import Celery

from django.conf import settings
from xvfbwrapper import Xvfb
xvfb = Xvfb(width=1280, height=720)
xvfb.start()

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanagement.settings')

app = Celery()

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
