# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'odoo'

import unittest


class FundHistoryTestCase(unittest.TestCase):

    def setUp(self):
        self.extra = dict()
        self.extra['url'] = "http://fund.eastmoney.com/f10/jjjz_288002.html"
        self.extra['timeout'] = 600
        self.extra['tag'] = "label"
        self.extra['text'] = u'下一页'
        self.extra['continue'] = True
        self.extra['code'] = '288002'

    def test_something(self):
        from spider.extension.facade import WorkerFacade
        WorkerFacade.process_fund_history(self.extra)


if __name__ == '__main__':
    unittest.main()
