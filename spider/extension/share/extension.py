# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'

from spider.extension.generators import TableParser
from spider.framework.browser import JSDataGenerator
from spider.framework.storage import HBaseData
from public.utils import tables

from bs4 import BeautifulSoup

import re
import copy


class ShareDataGenerator(JSDataGenerator):
    """
    share holds
    """
    VISITED = "unvisited"

    def data(self):

        is_loop, data = super(ShareDataGenerator, self).data()
        if data:
            origin_data = data
            soup = BeautifulSoup(data, from_encoding='utf-8')
            div = soup.find("div", class_="fn_fund_invest_item")
            tbody = div.find("tbody")
            data = str(tbody)

            # collection return data with sub tasks
            try:
                from admintasks import tasks
                sub_extra = copy.deepcopy(self.extra)
                sub_extra['html'] = origin_data
                tasks.fund_return_task.apply_async((sub_extra), countdown=2)
            except Exception as e:
                print e

        return is_loop, data


class ShareData(HBaseData):
    """

    """
    def __init__(self, code, name, url, amount, percentage, fund):
        self.code = code
        self.name = name
        self.url = url
        self.percentage = percentage
        self.amount = amount
        self.fund = fund

    def table(self):
        return tables.TABLE_SHARE

    def row(self):
        return tables.ROW_ID.format(self.fund, self.code)

    def columns(self):
        return {tables.COLUMN_FAMILY: {tables.CODE: self.code, tables.NAME: self.name,
                                       tables.PERCENTAGE: self.percentage,
                                       tables.AMOUNT: self.amount,
                                       tables.URL: self.url}}


class ShareTableParser(TableParser):
    
    def __init__(self):
        self.generator = None
    
    def parse(self, string, generator=None):
        self.generator = generator
        
        return super(ShareTableParser, self).parse(string, generator)

    def parse_item(self, tds):
        a = tds[0].find("a")
        url = a['href']
        return ShareData(re.findall('\d+', url.split('/')[-1][1:])[0],
                         a.string,
                         url,
                         tds[1].string,
                         tds[3].string,
                         self.generator.extra['fund'])
