# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'


from spider.framework.storage import HBaseData
from spider.extension.generators import TableBodyDataGenerator, TableParser

from public.utils import tables, tools
#
# class Industry(TableBodyDataGenerator):
#
#
#     def __init__(self, extra):
#         super(Industry, self).__init__(extra)
#         # self.class_ = "tab1"


class IndustryData(HBaseData):

    def __init__(self, name, amplitude, flow, major):
        self.name = name
        self.amplitude = amplitude
        self.flow = flow
        self.major = major

    def table(self):

        return tables.TABLE_INDUSTRY

    def row(self):

        return tables.ROW_ID.format(self.name, tools.current_date())

    def columns(self):

        return {tables.NAME: self.name, tables.AMPLITUDE: self.amplitude, tables.FLOW: self.flow, tables.MAJOR: self.major}


class IndustryParser(TableParser):


    def parse_item(self, tds):

        return IndustryData(tds[1].string, tds[3].string, tds[4].string, tds[14].string)



