# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'odoo'

import unittest


class FundTestCase(unittest.TestCase):

    def setUp(self):

        self.extra = dict()
        # self.extra['url'] = "http://fund.eastmoney.com/fund.html"
        self.extra['url'] = "http://quotes.money.163.com/"
        self.extra['timeout'] = 10
        self.extra['continue'] = True
        self.extra['header_text'] = u'基金净值'
        self.extra['sub_domain'] = u'股票型'
        self.extra['query'] = "'#FN'"
        self.extra['text'] = u'下一页'
        self.extra['tag'] = 'a'
        # self.extra['class'] = 'dbtable'
        self.extra['show'] = True

    def test_worker(self):
        from spider.extension.facade import WorkerFacade
        WorkerFacade.process_fund_list(self.extra)


if __name__ == '__main__':
    unittest.main()
