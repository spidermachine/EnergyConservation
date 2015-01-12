# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'


class Storage(object):
    """

    """
    def save(self, data):
        pass

    def batch_save(self, data):
        pass

    def fetch(self, table, column, value, operation, columns=[], size=1):
        pass


class HBaseData(object):
    """
    data need to save
    """
    def table(self):
        pass

    def row(self):
        pass

    def columns(self):
        pass

