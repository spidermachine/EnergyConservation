# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'cping.ju'

from public.utils import tables
from spider.framework.storage import HBaseData
from spider.extension.generators import TableBodyDataGenerator, TableParser

class YJLBodyDataGenerator(TableBodyDataGenerator):

    def __init__(self, extra):
        super(YJLBodyDataGenerator, self).__init__(extra)
        self.class_ = "table01"


class YJLData(HBaseData):

    def __init__(self, name=None, code=None, price=None, date_string=None):
        self.name = name
        self.code = code
        self.price = price
        self.data_string = date_string

    def table(self):
        return tables.TABLE_FINANCE

    def row(self):
        return tables.ROW_ID.format(self.code, self.data_string)

    def columns(self):
        return {tables.COLUMN_FAMILY:{tables.NAME: self.name, tables.CODE: self.code,
                                      tables.PRICE: self.price,
                                      tables.DATE: self.data_string}}


class YJLParser(TableParser):

    def parse_item(self, tds):

        return YJLData(name=tds[1].string, code=tds[0].string, price=tds[2].string,
                       date_string=tds[3].string)