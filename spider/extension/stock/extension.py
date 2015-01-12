# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'

from spider.extension.generators import TableBodyDataGenerator, TableParser
from spider.framework.storage import HBaseData
from public.utils import tables, tools

import time

from spynner.browser import SpynnerTimeout

class StockDataGenerator(TableBodyDataGenerator):
    def __init__(self, extra):

        super(StockDataGenerator, self).__init__(extra)
        self.children = []
        self.load_header()

    def load_header(self):
        """
        click the button named "more", load all of industry
        """
        web_elements = self.browser.webframe.findAllElements(self.extra['tag'])
        is_load_header = False
        for element in web_elements:
            # found the next page
            if str(element.toInnerXml()).strip() == self.extra['more_text'] and\
                            self.extra['query'] in element.attribute("href"):
                # trigger the link and load the next page
                # element.evaluateJavaScript("this.click()")
                try:
                    self.browser.wk_click_element(element, wait_load=True, timeout=10)
                except SpynnerTimeout as e:
                    print e
                # self.browser.wait_load(timeout=self.extra['timeout'])
                is_load_header = True
                break

        if is_load_header:

            element = self.browser.webframe.findFirstElement("div[class='bread-crumbs-details']")

            if element:
                self.children = [e for e in element.findAll("a")]

    def load_next_page(self):

        # super(StockDataGenerator, self).load_next_page()

        self.is_load = False
        # sleep 3 seconds, if no command
        sleep = self.extra.get('sleep', 3)
        time.sleep(sleep)

        # find link of next page
        hsRank = self.browser.webframe.findFirstElement("div[id='hsRank']")
        element = hsRank.findFirst("a[class='pages_flip']")
        if element and (str(element.toInnerXml()).strip() == self.extra['text']):
            try:
                self.browser.wk_click_element(element, wait_load=True, timeout=10)
            except SpynnerTimeout as e:
                print e
            self.is_load = True


        if not self.is_load:
            if len(self.children) > 0:
                element = self.children.pop(0)
                # element.evaluateJavaScript("this.click()")
                # self.browser.wait_load(timeout=self.extra['timeout'])
                try:
                    self.browser.wk_click_element(element, wait_load=True, timeout=10)
                except SpynnerTimeout as e:
                    print e
                self.is_load = True


class StockJournalData(HBaseData):
    def __init__(self, code, name, date, price, delta_ratio, delta, start, last, height, low, count, amount, stto,
                 amount_ratio, appoint_than, amplitude, PE, LTSZ, MC, ret_per, net_income, major_income, category, url):
        """
        名称  价格 日期 涨跌幅 涨跌额 今开 昨收 最高 最低 成交量 成交额 换手率 量比 委比 振幅 市盈率 流通市值 总市值 每股收益 净利润 主营收 类别 url
        """
        self.code = code
        self.name = name
        self.date = date
        self.price = price
        self.delta_ratio = delta_ratio
        self.delta = delta
        self.start = start
        self.last = last
        self.height = height
        self.low = low
        self.count = count
        self.amount = amount
        self.stto = stto
        self.amount_ratio = amount_ratio
        self.appoint_than = appoint_than
        self.amplitude = amplitude
        self.pe = PE
        self.LTSZ = LTSZ
        self.MC = MC
        self.ret_per = ret_per
        self.net_income = net_income
        self.major_income = major_income
        self.category = category
        self.url = url

    def table(self):
        return tables.TABLE_STOCK

    def row(self):
        return tables.ROW_ID.format(self.code, self.date)

    def columns(self):
        return {tables.COLUMN_FAMILY: {tables.CODE: self.code, tables.NAME: self.name,
                                       tables.DATE: self.date, tables.PRICE: self.price,
                                       tables.DELTA_RATIO: self.delta_ratio, tables.DELTA: self.delta,
                                       tables.START: self.start, tables.LAST: self.last,
                                       tables.HEIGHT: self.height, tables.LOW: self.low,
                                       tables.COUNT: self.count, tables.STTO: self.stto,
                                       tables.AMOUNT_RATIO: self.amount_ratio, tables.APPOINT_THAN: self.appoint_than,
                                       tables.AMPLITUDE: self.amplitude, tables.PE: self.pe,
                                       tables.LTSZ: self.LTSZ, tables.MC: self.MC,
                                       tables.RET_PER: self.ret_per, tables.NET_INCOME: self.net_income,
                                       tables.MAJOR_INCOME: self.major_income, tables.CATEGORY: self.category,
                                       tables.URL: self.url}}


class StockTableParser(TableParser):
    def __init__(self):
        self.generator = None

    def parse(self, string, generator=None):
        self.generator = generator

        return super(StockTableParser, self).parse(string, self.generator)

    def parse_item(self, tds):
        a = tds[1].find("a")

        return StockJournalData(a.string, tds[2].find("a").string,
                                self.generator.extra.get('date', tools.current_date()),
                                tds[3].string, tds[4].string, tds[5].string,
                                tds[7].string, tds[8].string, tds[9].string,
                                tds[10].string, tds[11].string, tds[12].string,
                                tds[13].string, tds[14].string, tds[15].string,
                                tds[16].string, tds[17].string, tds[18].string,
                                tds[19].string, tds[20].string, tds[21].string,
                                tds[22].string, self.generator.extra.get('category', "未知"), a['href'])