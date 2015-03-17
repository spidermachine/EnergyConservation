# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'

import unittest


class BSTestCase(unittest.TestCase):

    def setUp(self):
        self.extra = dict()
        self.extra['url'] = "http://quotes.money.163.com/#query=radar"
        self.extra['continue'] = True
        self.extra['tag'] = "a"
        self.extra['text'] = u"下一页"
        self.extra['timeout'] = 10

        from xvfbwrapper import Xvfb
        self.xvfb = Xvfb(width=1280, height=720)
        self.xvfb.start()

    def test_buy_sales(self):

        from spider.extension.facade import WorkerFacade

        WorkerFacade.process_buy_sales(self.extra)


if __name__ == '__main__':
    unittest.main()
