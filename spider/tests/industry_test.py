# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'odoo'

import unittest


class IndustryTestCase(unittest.TestCase):

    def setUp(self):
        self.extra = dict()
        self.extra['url'] = 'http://data.10jqka.com.cn/funds/hyzjl'
        self.extra['continue'] = True
        self.extra['tag'] = 'a'
        self.extra['text'] = u'下一页'
        self.extra['class'] = 'm_table'
        self.extra['timeout'] = 600
        self.extra['show'] = True

    def test_industry(self):

        from spider.extension.facade import WorkerFacade
        WorkerFacade.process_industry(self.extra)


if __name__ == '__main__':
    unittest.main()
