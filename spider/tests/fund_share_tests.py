# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'odoo'

import unittest


class FundShareTestCase(unittest.TestCase):

    def setUp(self):
        self.extra = dict()
        self.extra['url'] = "http://fund.eastmoney.com/f10/ccmx_288002.html"
        self.extra['timeout'] = 600
        self.extra['fund'] = '288002'


    def test_something(self):
        from spider.extension.facade import WorkerFacade
        WorkerFacade.process_share(self.extra)


if __name__ == '__main__':
    unittest.main()
