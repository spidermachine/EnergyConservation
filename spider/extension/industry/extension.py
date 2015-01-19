# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'

from spider.framework.storage import HBaseData
from spider.extension.generators import TableParser

from public.utils import tables, tools


class IndustryData(HBaseData):
    def __init__(self, name, url, amplitude, in_flow, out_flow, balance):
        self.name = name
        self.url = url
        self.amplitude = amplitude
        self.in_flow = in_flow
        self.out_flow = out_flow
        self.balance = balance

    def table(self):
        return tables.TABLE_INDUSTRY

    def row(self):
        return tables.ROW_ID.format(self.name, tools.current_date())

    def columns(self):
        return {tables.COLUMN_FAMILY: {tables.NAME: self.name,
                                       tables.URL: self.url,
                                       tables.AMPLITUDE: self.amplitude,
                                       tables.OUT_FLOW: self.out_flow,
                                       tables.IN_FLOW: self.in_flow,
                                       tables.BALANCE: self.balance}}


class IndustryParser(TableParser):
    def parse_item(self, tds):
        name, url = self.parse_tag_a(tds[1])
        return IndustryData(name, url, tds[4].string, tds[5].string, tds[6].string, tds[7].string)


