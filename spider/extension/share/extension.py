# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'cping.ju'

from spider.extension.generators import TableParser
from spider.framework.browser import JSDataGenerator
from spider.framework.storage import HBaseData

from bs4 import BeautifulSoup

import time

class ShareDataGenerator(JSDataGenerator):
    """
    share holds
    """
    def __init__(self, extra):
        super(ShareDataGenerator, self).__init__(extra)

    def data(self):

        is_loop, data = super(ShareDataGenerator, self).data()
        if data:
            soup = BeautifulSoup(data, from_encoding='utf-8')
            div = soup.find("div", id="cctable")
            # table = soup.find("div", class_="box").find("table")
            tbody = div.find("tbody")
            data = str(tbody)

        return is_loop, data


class ShareData(HBaseData):
    """

    """
    def __init__(self, code, name, percentage, amount, fund):
        self.code = code
        self.name = name
        self.percentage = percentage
        self.amount = amount
        self.fund = fund

    def table(self):
        return "share"

    def row(self):
        return "{1}_{2}".format(self.fund, int(round(time.time() * 1000)))

    def columns(self):
        return {"cf": {"code": self.code, "name": self.name, "percentage": self.percentage, "amount": self.amount}}


class ShareTableParser(TableParser):
    
    def __init__(self):
        self.generator = None
    
    def parse(self, string, generator=None):
        self.generator = generator
        
        return super(ShareTableParser, self).parse(string, generator)
        

    def parse_item(self, tds):

        return ShareData(tds[1].string, tds[2].string, tds[6].string, tds[7].string, self.generator.extra['fund'])
