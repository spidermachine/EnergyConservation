__author__ = 'keping'

import unittest


class GradeTestCase(unittest.TestCase):

    def setUp(self):
        self.extra = dict()
        self.extra['url'] = 'http://cn.morningstar.com/quickrank/default.aspx'
        self.extra['timeout'] = 600
        self.extra['continue'] = True
        self.extra['text'] = u'&gt;'
        self.extra['tag'] = u'a'
        self.extra['id'] = 'ctl00_cphMain_gridResult'
        self.extra['show'] = True

        from xvfbwrapper import Xvfb
        self.xvfb = Xvfb(width=1280, height=720)
        self.xvfb.start()

    def tearDown(self):
        self.xvfb.stop()

    def test_grade(self):
        from spider.extension.facade import WorkerFacade
        WorkerFacade.process_fund_grade(self.extra)


if __name__ == '__main__':
    unittest.main()
