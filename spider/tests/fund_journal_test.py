__author__ = 'odoo'

import unittest


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.extra = dict()
        self.extra['url'] = 'http://fund.eastmoney.com/fund.html'
        self.extra['timeout'] = 600
        self.extra['continue'] = False


    def test_something(self):

        from spider.extension.facade import WorkerFacade
        WorkerFacade.process_fund_journal(self.extra)


if __name__ == '__main__':
    unittest.main()
