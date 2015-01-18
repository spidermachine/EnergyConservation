# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping'

import unittest


class StockGradeTestCase(unittest.TestCase):

    def setUp(self):
        self.extra = dict()
        self.extra['url'] = "http://vip.stock.finance.sina.com.cn/q/go.php/vIR_SumRating/index.phtml"
        self.extra['timeout'] = 600
        self.extra['tag'] = 'a'
        self.extra['text'] = u'下一页'
        self.extra['class'] = 'list_table'

    def test_stock_grade(self):
        from spider.extension.facade import WorkerFacade
        WorkerFacade.process_stock_grade(self.extra)


if __name__ == '__main__':
    unittest.main()
