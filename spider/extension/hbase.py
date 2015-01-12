# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'


from spider.framework.storage import Storage
from public.utils import tables

from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from thrifthbase.hbase import Hbase

# from starbase.client import connection
# class HBaseStorage(Storage):
#     """
#     storage for HBase
#     """
#     def __new__(cls, *args, **kwargs):
#
#         if not hasattr(cls, "instance"):
#             cls.instance = super(HBaseStorage, cls).__new__(cls, *args, **kwargs)
#
#         return cls.instance
#
#     def __init__(self, host='127.0.0.1', port='9999', user=None, password=None, secure=False):
#
#         if not hasattr(self, "c"):
#             self.c = connection.Connection(host, port, user, password, secure)
#
#     def save(self, data):
#
#         if issubclass(type(data), HBaseData):
#             table = self.c.table(data.table())
#             table.insert(data.row(), data.columns())
#
#     def fetch(self, attribute):
#
#         t = self.c.table(attribute['table'])
#         return t.fetch_all_rows(perfect_dict= {}, filter_string=attribute['filter'], scanner_config=attribute['scanner_config'])
#
#
#     def batch_save(self, data):
#
#         if isinstance(data, list):
#             b = self.c.table(data[0].table()).batch()
#             if b:
#                 for item in data:
#                     b.insert(item.row(), item.columns())
#                 b.commit(finalize=True)


class ThriftHBaseStorage(Storage):

    INSTANCE = None

    def __new__(cls, *args, **kwargs):

        if not hasattr(cls, "instance"):
            cls.instance = super(ThriftHBaseStorage, cls).__new__(cls, *args, **kwargs)

        return cls.instance

    @staticmethod
    def get_instance():

        if not ThriftHBaseStorage.INSTANCE:
            ThriftHBaseStorage.INSTANCE = ThriftHBaseStorage()
        return ThriftHBaseStorage.INSTANCE

    def __init__(self, host='127.0.0.1', port='9050'):

        if not hasattr(self, "transport"):
            self.host = host
            self.port = port
            self.transport = TTransport.TBufferedTransport(TSocket.TSocket(self.host, self.port))
            self.client = Hbase.Client(TBinaryProtocol.TBinaryProtocolAccelerated(self.transport))
            self.transport.open()

    def reopen(self):
        self.transport.close()
        self.transport = TTransport.TBufferedTransport(TSocket.TSocket(self.host, self.port))
        self.client = Hbase.Client(TBinaryProtocol.TBinaryProtocolAccelerated(self.transport))
        self.transport.open()

    def save(self, data):
        columns = data.columns()[tables.COLUMN_FAMILY]
        self.update(data.table(), data.row(), columns)
        # mutations = [Hbase.Mutation(column="{0}:{1}".format(tables.COLUMN_FAMILY, k), value=v.strip()) for k, v in columns]
        # self.client.mutateRow(data.table(), data.row(), mutations)

    def batch_save(self, data):
        mutations = []
        for item in data:
            columns = item.columns()[tables.COLUMN_FAMILY]
            mutations.append(Hbase.BatchMutation(row=item.row(),
                                                 mutations=[Hbase.Mutation(column="{0}:{1}".format(tables.COLUMN_FAMILY, k), value=v.strip()) for k, v in columns]))
        self.client.mutateRows(data[0].table(), mutations)

    def __delete__(self, instance):
        
        super(ThriftHBaseStorage, self).__delete__(instance)

        self.transport.close()
        
    def fetch(self, table, column, value, operation, columns=[], size=1):
        scan = Hbase.TScan(columns=columns,
                           filterString="(SingleColumnValueFilter ('{0}', '{1}', {2}, '{3}'))".format(tables.COLUMN_FAMILY, column, operation, value))
        scannerId = self.client.scannerOpenWithScan(table, scan)
        rows = self.client.scannerGetList(scannerId, size)
        self.client.scannerClose(scannerId)
        return rows

    def update(self, table, row, attributes={}):

        columns = attributes
        mutations = [Hbase.Mutation(column="{0}:{1}".format(tables.COLUMN_FAMILY, k), value=v.strip()) for k, v in columns]
        self.client.mutateRow(table, row, mutations)