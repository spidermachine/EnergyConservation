__author__ = 'keping'

import unittest


class GradeTestCase(unittest.TestCase):

    def setUp(self):
        self.extra = dict()
        self.extra['url'] = 'http://cn.morningstar.com/quickrank/default.aspx'
        self.extra['timeout'] = 600
        self.extra['continue'] = True
        self.extra['text'] = u'>'
        self.extra['tag'] = u'a'



    def test_grade(self):

        from spider.extension.facade import WorkerFacade
        WorkerFacade.process_fund_grade(self.extra)


if __name__ == '__main__':
    unittest.main()
