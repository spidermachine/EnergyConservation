# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'odoo'

import unittest
from public.utils import memcache, tables

class IndustryTestCase(unittest.TestCase):

    def setUp(self):
        self.extra = dict()
        self.extra['url'] = 'http://data.10jqka.com.cn/funds/ggzjl/'
        self.extra['continue'] = True
        self.extra['tag'] = 'a'
        self.extra['text'] = u'下一页'
        self.extra['class'] = 'm_table'
        self.extra['timeout'] = 15
        # self.extra['show'] = True
        self.extra['wait'] = True

        from xvfbwrapper import Xvfb
        self.xvfb = Xvfb(width=1280, height=720)
        self.xvfb.start()

    def tearDown(self):
        self.xvfb.stop()

    def test_industry(self):

        if not memcache.is_table_collected(tables.TABLE_SHARE_MONEY):
            from spider.extension.facade import WorkerFacade
            WorkerFacade.process_money_flow(self.extra)
            memcache.table_collected(tables.TABLE_SHARE_MONEY)


if __name__ == '__main__':
    unittest.main()
