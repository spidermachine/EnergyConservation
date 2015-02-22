__author__ = 'geu'

import unittest
from thrifthbase.hbase.ttypes import *

class MyTestCase(unittest.TestCase):
    def test_something(self):
        from thrift.transport import TSocket
        from thrift.transport import TTransport
        from thrift.protocol import TBinaryProtocol
        from thrifthbase.hbase import Hbase

        transport = TSocket.TSocket('127.0.0.1', 9090)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = Hbase.Client(protocol)
        transport.open()
        print client.getTableNames()

if __name__ == '__main__':
    unittest.main()
