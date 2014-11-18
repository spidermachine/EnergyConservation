__author__ = 'odoo'

import unittest


class FundTestCase(unittest.TestCase):

    def setUp(self):

        self.extra = dict()
        self.extra['url'] = "http://fund.eastmoney.com/fund.html"
        self.extra['timeout'] = "600"
        self.extra['continue'] = False
        # self.extra['show'] = True

    def test_worker(self):
        from spider.extension.facade import WorkerFacade
        WorkerFacade.process_fund_list(self.extra)


if __name__ == '__main__':
    unittest.main()
