# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping'

import unittest


class YJLTestCase(unittest.TestCase):

    def setUp(self):

        self.extra = {}
        self.extra['url'] = "http://www.bankofshanghai.com/WebServlet?go=bank_sellfund_pg_Banking&code=hcyjl"
        self.extra['timeout'] = 600
        self.extra['tag'] = "a"
        self.extra['text'] = u"下一页"
        self.extra['continue'] = True
        self.extra['class'] = 'table01'

        from django.conf import settings
        from xvfbwrapper import Xvfb
        self.xvfb = Xvfb(width=1280, height=720)
        self.xvfb.start()

    # def tearDown(self):
    #     self.xvfb.stop()

    def test_worker(self):
        from spider.extension.facade import WorkerFacade
        WorkerFacade.process_yjl(self.extra)



if __name__ == '__main__':
    unittest.main()
