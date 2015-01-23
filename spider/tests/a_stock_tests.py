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
        self.extra['more_text'] = u"沪市A股"
        self.extra['timeout'] = 600
        self.extra['query'] = "#query=EQA_EXCHANGE_CNSESH&DataType=HS_RANK"
        self.extra['class'] = "stocks-info-table"
        self.extra['show'] = True
        self.extra['need'] = False

    def test_stock(self):
        from spider.extension.facade import WorkerFacade
        WorkerFacade.process_a_stock(self.extra)

if __name__ == '__main__':
    unittest.main()
