# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'

import unittest


class BSTestCase(unittest.TestCase):

    def setUp(self):
        self.extra = dict()
        self.extra['url'] = "http://quotes.money.163.com"
        self.extra['continue'] = True
        self.extra['tag'] = "a"
        self.extra['text'] = u"下一页"
        self.extra['more_text'] = u"实时大单"
        self.extra['timeout'] = 20
        self.extra['show'] = True
        self.extra['need'] = False
        self.extra['query'] = "#query=RTDD&DataType=realtimeDaDan"

    #     from xvfbwrapper import Xvfb
    #     self.xvfb = Xvfb(width=1280, height=720)
    #     self.xvfb.start()
    #
    # def tearDown(self):
    #     self.xvfb.stop()

    def test_buy_sales(self):

        from spider.extension.facade import WorkerFacade

        WorkerFacade.process_buy_sales(self.extra)


if __name__ == '__main__':
    unittest.main()
