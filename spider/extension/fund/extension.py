# !/usr/bin/python
# vim: set fileencoding=utf8 :
#

__author__ = 'keping.chu'


from spider.extension.generators import TableParser, TableBodyDataGenerator, TableDataGenerator
from spider.framework.storage import HBaseData
from spider.framework.browser import DataGenerator
from spider.extension import tags
from public.utils import tables

import time
from bs4 import BeautifulSoup

from spynner.browser import SpynnerTimeout


class FundBodyDataGenerator(TableBodyDataGenerator):

    def __init__(self, extra):

        super(FundBodyDataGenerator, self).__init__(extra)
        self.load_header()

    def load_header(self):
        """
        click the button named "more", load all of industry
        """
        web_elements = self.browser.webframe.findAllElements(self.extra['tag'])
        is_load_header = False
        for element in web_elements:
            # found the next page
            if str(element.toInnerXml()).strip() == self.extra['header_text'] and\
                            self.extra['query'] in element.attribute("href"):
                # trigger the link and load the next page
                # element.evaluateJavaScript("this.click()")
                try:
                    self.browser.wk_click_element(element, wait_load=True, timeout=self.extra['timeout'])
                except SpynnerTimeout as e:
                    print e
                # self.browser.wait_load(timeout=self.extra['timeout'])
                is_load_header = True
                break

        if is_load_header:

            element = self.browser.webframe.findFirstElement("div[id='fnRanks']")

            if element:
                element = element.findFirst("ul[class='mod-title-bar']")
                for ae in element.findAll("a"):
                    # print str(element.toInnerXml()).strip()
                    if str(ae.toInnerXml()).strip() == self.extra['sub_domain']:
                        try:
                            self.browser.wk_click_element(ae, wait_load=True, timeout=self.extra['timeout'])
                        except SpynnerTimeout as e:
                            print e
                        self.is_load = True
                        break

    def load_next_page(self):

        # super(StockDataGenerator, self).load_next_page()

        self.is_load = False
        # sleep 3 seconds, if no command
        sleep = self.extra.get('sleep', 3)
        time.sleep(sleep)

        # find link of next page
        hsRank = self.browser.webframe.findFirstElement("div[id='fnRanks']")
        element = hsRank.findAll("a[class='pages_flip']").last()
        if element and (str(element.toInnerXml()).strip() == self.extra['text']):
            try:
                self.browser.wk_click_element(element, wait_load=True, timeout=10)
            except SpynnerTimeout as e:
                print e
            self.is_load = True

    def data(self):
        is_loop, data = super(TableDataGenerator, self).data()
        if data:
            soup = BeautifulSoup(data, from_encoding='uft-8')
            soup = soup.find("div", id='fnRanks')
            data = soup.find("table", _quotedata_query_='STYPE:FDO;TYPE3:GPX')
            # if self.extra.get("id", None):
            #     data = soup.find(tags.table, id=self.extra['id'])
            # elif self.extra.get("class", None):
            #     data = soup.find(tags.table, class_=self.extra['class'])
            data = str(data.find(tags.tbody))
            data = str(data)
        return is_loop, data


class FundData(HBaseData):

    def __init__(self, code, name, url, amount, price, inc_rate):
        self.code = code.strip()
        self.name = name.strip()
        self.url = url.strip()
        self.amount = amount
        self.price = price
        self.inc_rate = inc_rate
        self.visited = 'unvisited'

    def row(self):

        return self.code

    def table(self):
        return tables.TABLE_FUND

    def columns(self):

        return {tables.COLUMN_FAMILY: {tables.CODE: self.code,
                                       tables.NAME: self.name,
                                       tables.URL: self.url,
                                       tables.AMOUNT: self.amount,
                                       tables.PRICE: self.price,
                                       tables.INC_RATE:self.inc_rate,
                                       tables.TABLE_VISITED: self.visited}}


class FundParser(TableParser):

    def parse_item(self, tds):
        try:
            a = tds[2].find("a")
            return FundData(a.string, tds[3].find("a").string, a["href"], tds[8].string, tds[4].string, tds[5].string)
        except Exception as e:
            print e
            return None


class FundRetGenerator(TableBodyDataGenerator):
    """
    return of fund
    """
    def __init__(self, extra):
        self.extra = extra
        # super(DataGenerator, self).__init__(extra)

    def data(self):

        is_loop = False
        data = self.extra['html']
        if data:
            soup = BeautifulSoup(data, from_encoding='utf-8')
            div = soup.find("div", class_="fn_fund_achive")
            tbody = div.find("tbody")
            data = str(tbody)

        return is_loop, data


class FundRetData(HBaseData):
    """
    :return data of fund
    """
    def __init__(self, code, ret_week, ret_month, ret_season, ret_half_year, ret_year):

        self.code = code.strip()
        self.ret_week = ret_week
        self.ret_month = ret_month
        self.ret_season = ret_season
        self.ret_half_year = ret_half_year
        self.ret__year = ret_year


    def row(self):

        return self.code

    def table(self):

        return tables.TABLE_FUND

    def columns(self):

        return {tables.COLUMN_FAMILY: {tables.CODE: self.code,
                                       tables.RET_WEEK: self.ret_week,
                                       tables.RET_MONTH: self.ret_month,
                                       tables.RET_HALF_YEAR: self.ret_half_year,
                                       tables.RET_YEAR: self.ret__year}}


class FundRetParser(TableParser):

    def parse(self, string, generator=None):

        items = []
        soup = BeautifulSoup(string, from_encoding="utf-8")
        tr = soup.find(tags.tr)
        tds = tr.find_all(tags.td)
        item = self.parse_item(tds)
        if item:
            if generator:
                item.code = generator.extra['fund']
            items.append(item)

        return items

    def parse_item(self, tds):

        return FundRetData("",
                           tds[1].string,
                           tds[2].string,
                           tds[3].string,
                           tds[4].string,
                           tds[5].string)

