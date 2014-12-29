__author__ = 'odoo'

import unittest


class IndustryTestCase(unittest.TestCase):

    def setUp(self):
        self.extra = dict()
        self.extra['url'] = 'http://data.eastmoney.com/bkzj/hy.html'
        self.extra['continue'] = False
        self.extra['class'] = 'tab1'
        self.extra['timeout'] = 600

    def test_industry(self):

        from spider.extension.facade import WorkerFacade
        WorkerFacade.process_industry(self.extra)


if __name__ == '__main__':
    unittest.main()
