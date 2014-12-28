# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'cping.ju'


from spider.extension.generators import TableBodyDataGenerator, TableParser
from spider.framework.storage import HBaseData
from spider.extension import tags
from public.utils import tables

from bs4 import BeautifulSoup

import re


class GradeDataGenerator(TableBodyDataGenerator):

    def __init__(self, extra):

        super(GradeDataGenerator, self).__init__(extra)
        self.class_ = "ctl00_cphMain_gridResult"


class GradeData(HBaseData):

    def __init__(self, code, score, ret):

        self.code = code
        self.score = score
        self.ret = ret

    def table(self):
        return tables.TABLE_GRADE

    def row(self):
        return self.code

    def columns(self):

        return {tables.COLUMN_FAMILY: {tables.CODE: self.code, tables.GRADE: self.score}}


class GradeDataParser(TableParser):

    def parse(self, string, generator=None):
        items = []
        soup = BeautifulSoup(string, from_encoding="utf-8")
        for tr in soup.find_all(tags.tr)[1:]:
            tds = tr.find_all(tags.td)
            item = self.parse_item(tds)
            if item:
                # stop load data
                if item.score == 0 and generator != None:
                    generator.extra['continue'] = False
                    break
                items.append(item)
        return items

    def parse_item(self, tds):

        return GradeData(tds[2].find('a').string, re.findall(r'\d+',tds[5].find('img')['src'])[0], tds[10].string)
