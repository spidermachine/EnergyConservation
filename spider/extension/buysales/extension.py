# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'


from spider.framework.browser import NextPageDataGenerator
from spider.extension.generators import TableParser
from spider.framework.storage import HBaseData
from public.utils import tables, tools

from bs4 import BeautifulSoup

from spider.extension import tags
import time
from spynner.browser import SpynnerTimeout


class BSTableBodyDataGenerator(NextPageDataGenerator):

    def __init__(self, extra):

        super(BSTableBodyDataGenerator, self).__init__(extra)

    def data(self):

        is_loop, data = super(BSTableBodyDataGenerator, self).data()
        if data:
            soup = BeautifulSoup(data, from_encoding='uft-8')
            data = soup.find("div", class_="panelContentWrap").find(tags.table, class_="ID_table realtimeRadar-info-table stocks-info-table")
            data = str(data.find(tags.tbody))
        return is_loop, data

    def load_next_page(self):

        self.is_load = False
        # sleep 3 seconds, if no command
        sleep = self.extra.get('sleep', 3)
        time.sleep(sleep)

        # find link of next page
        radarCon = self.browser.webframe.findFirstElement("div[id='radarCon']")
        elementList = radarCon.findAll("a[class='pages_flip']")

        for element in elementList:
            # print str(element.toInnerXml()).strip()
            # found the next page
            if str(element.toInnerXml()).strip() == self.extra.get('text', u'下一页'):
                # trigger the link and load the next page
                try:
                    self.browser.wk_click_element(element, wait_load=self.extra.get("wait", True),
                                                  timeout=self.extra.get('timeout', 10))
                except SpynnerTimeout as e:
                    print e
                    if not self.extra.get('ignore_timeout', True):
                        raise e

                self.is_load = True
                break


class BuySalesData(HBaseData):

    def __init__(self, tradetime, code, name, buy_sales, amount, price, amplitude):

        self.tradetime = tradetime
        self.code = code
        self.name = name
        self.buy_sales = buy_sales
        self.amount = amount
        self.price = price
        self.amplitude = amplitude

    def table(self):
        return tables.TABLE_BUY_SALES

    def row(self):
        return tables.ROW_ID.format(self.code, tools.current_date() + "_" + self.tradetime)

    def columns(self):

        return {tables.COLUMN_FAMILY: {
            tables.TRADE_TIME: self.tradetime,
            tables.CODE: self.code,
            tables.NAME: self.name,
            tables.BUY_OR_SALES: self.buy_sales,
            tables.AMOUNT: self.amount,
            tables.PRICE: self.price,
            tables.AMPLITUDE: self.amplitude
        }}


class BuySalesParser(TableParser):

    def parse_item(self, tds):

        return BuySalesData(tds[1].string,
                            self.parse_tag_a(tds[2])[1],
                            self.parse_tag_a(tds[3])[1],
                            tds[4].string,
                            tds[5].string,
                            tds[6].string,
                            tds[7].string)