# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping'

import unittest


class StockTestCase(unittest.TestCase):

    def setUp(self):
        self.extra = dict()
        self.extra['url'] = "http://quotes.money.163.com/"
        self.extra['continue'] = True
        self.extra['tag'] = "a"
        self.extra['text'] = u"下一页"
        self.extra['timeout'] = 600
        self.extra['query'] = "#query=hy"
        self.extra['class'] = "stock-info-table"


    def test_stock(self):
        from spider.extension.facade import WorkerFacade
        WorkerFacade.process_stock(self.extra)

if __name__ == '__main__':
    unittest.main()
