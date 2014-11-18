# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'cping.ju'


from starbase.client import connection


class Storage(object):
    """

    """
    def save(self, data):
        pass

    def batch_save(self, data):
        pass


class HBaseStorage(Storage):
    """
    storage for HBase
    """
    def __new__(cls, *args, **kwargs):

        if not hasattr(cls, "instance"):
            cls.instance = super(HBaseStorage, cls).__new__(cls, *args, **kwargs)

        return cls.instance

    def __init__(self, host='127.0.0.1', port='9999', user=None, password=None, secure=False):

        if not hasattr(self, "c"):
            self.c = connection.Connection(host, port, user, password, secure)

    def save(self, data):

        if issubclass(type(data), HBaseData):
            table = self.c.table(data.table())
            table.insert(data.row(), data.columns())

    def batch_save(self, data):

        if isinstance(data, list):
            b = self.c.table(data[0].table()).batch()
            if b:
                for item in data:
                    b.insert(item.row(), item.columns())
                b.commit(finalize=True)


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

