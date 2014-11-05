# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'cping.ju'

from __future__ import absolute_import

import os

from celery import Celery

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanagement.settings')

app = Celery()

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
