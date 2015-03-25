# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'


from spider.extension.stock.extension import StockDataGenerator
from spider.extension.generators import TableParser, TableDataGenerator
from spider.framework.storage import HBaseData
from public.utils import tables, tools, memcache

from bs4 import BeautifulSoup

from spider.extension import tags
import time
from spynner.browser import SpynnerTimeout


class BigBillTableBodyDataGenerator(StockDataGenerator):

    def __init__(self, extra):

        super(BigBillTableBodyDataGenerator, self).__init__(extra)

    def data(self):

        is_loop, data = super(TableDataGenerator, self).data()
        if data:
            soup = BeautifulSoup(data, from_encoding='uft-8')
            data = soup.find("div", class_="panelContentWrap").find(tags.table, class_="ID_table stocks-info-table")
            data = str(data.find(tags.tbody))
        return is_loop, data

    def load_next_page(self):

        self.is_load = False
        # sleep 3 seconds, if no command
        sleep = self.extra.get('sleep', 3)
        time.sleep(sleep)

        # find link of next page
        radarCon = self.browser.webframe.findFirstElement("div[id='realtimeDaDanCon']")
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


class BigBillData(HBaseData):

    def __init__(self, code, name, tradetime, price, last_price, amplitude, amount, volume, buy_sales):

        self.code = code
        self.name = name
        self.tradetime = tradetime
        self.price = price
        self.last_price = last_price
        self.amplitude = amplitude
        self.amount = amount
        self.volume = volume
        self.buy_sales = buy_sales

    def table(self):
        return tables.TABLE_BUY_SALES

    def row(self):
        return tables.ROW_ID.format(self.code, time.time().real)

    def columns(self):
        return {tables.COLUMN_FAMILY: {

            tables.CODE: self.code,
            tables.NAME: self.name,
            tables.DATE: tools.current_date(),
            tables.TRADE_TIME: self.tradetime,
            tables.PRICE: self.price,
            tables.LAST_PRICE: self.last_price,
            tables.AMPLITUDE: self.amplitude,
            tables.AMOUNT: self.amount,
            tables.VOLUME: self.volume,
            tables.BUY_OR_SALES: self.buy_sales
        }}


class BigBillParser(TableParser):

    def parse_item(self, tds):

        return BigBillData(self.parse_tag_a(tds[1])[0],
                           self.parse_tag_a(tds[2])[0],
                           tds[3].string,
                           tds[4].string,
                           tds[5].string,
                           tds[6].string,
                           tds[7].string,
                           tds[8].string,
                           tds[9].string)

    def stop_parse(self, generator=None, item=None):

        code, time = memcache.get_big_bill()

        if code is None and time is None:

            memcache.set_big_bill(item.code, item.tradetime)
            generator.extra['item'] = (item.code, item.tradetime)
            return None

        # set stop item
        elif generator.extra.get('item', None):

            memcache.set_big_bill(item.code, item.tradetime)
            generator.extra['item'] = (code, time)

        # stop
        if generator.extra['item'][0] == item.code and generator.extra['item'][1] == item.tradetime:

            generator.extra['continue'] = False

            raise Exception('stop')
