# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'

import datetime
import os


def current_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def day_after_now(days=0):
    return (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d")


def send_mail(title, msg, sender, receiver):
    """
    用系统自带的命令发送电子邮件,紧限于文本
    """
    if not msg or (msg == 'None'):
        return
    command = u'echo "%s" | mail -s "%s" -a "From: %s" "%s"' % (msg, title, sender, receiver)
    os.popen(command.encode('utf8'))
