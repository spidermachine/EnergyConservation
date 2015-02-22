# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'

import datetime

def current_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def day_after_now(days=0):
    return (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d")
