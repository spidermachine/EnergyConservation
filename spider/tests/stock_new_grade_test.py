# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'geu'

import unittest


class StockNewGradeTestCase(unittest.TestCase):

    def setUp(self):
        self.extra = dict()
        self.extra['url'] = "http://vip.stock.finance.sina.com.cn/q/go.php/vIR_RatingNewest/index.phtml"
        self.extra['timeout'] = 60
        self.extra['tag'] = 'a'
        self.extra['text'] = u'下一页'
        self.extra['class'] = 'list_table'
        self.extra['show'] = False
        self.extra['continue'] = True
        self.extra['ignore_timeout'] = False
        self.extra['sleep'] = 20

        from xvfbwrapper import Xvfb
        self.xvfb = Xvfb(width=1280, height=720)
        self.xvfb.start()

    def tearDown(self):
        self.xvfb.stop()

    def test_stock_grade(self):
        from spider.extension.facade import WorkerFacade
        WorkerFacade.process_stock_new_grade(self.extra)


if __name__ == '__main__':
    unittest.main()
