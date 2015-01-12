# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'

from spider.framework.storage import Storage

class MysqlStorage(Storage):

    def save(self, data):
        data.save()

    def batch_save(self, data):
        type(data[0]).objects.bulk_create(data)
