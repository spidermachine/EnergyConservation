# !/usr/bin/python
# vim: set fileencoding=utf8 :
#

__author__ = 'cping.ju'


from spider.extension.generators import TableParser, TableBodyDataGenerator, TableDataGenerator
from spider.extension.share.extension import ShareTableParser
from spider.framework.storage import HBaseData
from spider.framework.browser import NextPageDataGenerator
from spider.extension import tags
from public.utils import tables


from bs4 import BeautifulSoup


# class FundBodyDataGenerator(TableBodyDataGenerator):
#     """
#     fund list
#     """
#     def __init__(self, extra):
#
#         super(FundBodyDataGenerator, self).__init__(extra)
#
#         # self.class_ = "dbtable"


class FundData(HBaseData):

    def __init__(self, code, name, url):
        self.code = code.strip()
        self.name = name.strip()
        self.url = url.strip()
        self.visited = 0

    def row(self):

        return self.code

    def table(self):
        return tables.TABLE_FUND

    def columns(self):

        return {tables.COLUMN_FAMILY: {tables.CODE: self.code,
                                       tables.NAME: self.name,
                                       tables.URL: self.url,
                                       tables.TABLE_VISITED: self.visited}}


class FundParser(TableParser):

    def parse_item(self, tds):
        try:
            a = tds[4].find("a")
            return FundData(tds[3].string, a.string, a["href"])
        except Exception as e:
            print e
            return None



class FundJournalGenerator(TableDataGenerator):

    def __init__(self, extra):

        super(FundJournalGenerator, self).__init__(extra)

        self.class_ = "dbtable"


class FundJournalData(HBaseData):
    """
    lasted price of fund
    """
    def __init__(self, code, date, price, percent):

        # self.name = name.strip()
        self.code = code.strip()
        self.date = date.strip()
        self.price = price.strip()
        # self.increase = increase.strip()
        self.percent = percent.strip()

    def row(self):

        return tables.ROW_ID.format(self.code, self.date)

    def table(self):

        return tables.TABLE_FUND_JOURNAL

    def columns(self):

        return {tables.COLUMN_FAMILY: {tables.CODE: self.code, tables.DATE: self.date,
                                       tables.PRICE: self.price,
                                       tables.PERCENT: self.percent}}


class FundJournalParser(TableParser):

    def __init__(self):
        self.date = None

    def parse(self, string, generator=None):

        soup = BeautifulSoup(string, from_encoding="utf-8")

        self.date = soup.find(tags.thead).find(tags.tr).find_all(tags.td)[6].string.strip()

        # delete header of table
        return super(FundJournalParser, self).parse(str(soup.find(tags.tbody)))

    def parse_item(self, tds):

        try:
            a = tds[4].find("a")
            return FundJournalData(tds[3].string, self.date,
                                tds[7].string, tds[10].string)
        except Exception as e:
            import traceback
            print traceback.format_exc()

        return None


class FundHistoryDataGenerator(NextPageDataGenerator):
    """
    history price of fund
    """
    def __init__(self, extra):
        super(FundHistoryDataGenerator, self).__init__(extra)

    def data(self):
        is_loop, data = super(FundHistoryDataGenerator, self).data()
        if data:
            soup = BeautifulSoup(data, from_encoding='utf-8')
            div = soup.find("div", id="jztable")
            # table = div.find("table")
            tbody = div.find("tbody")
            data = str(tbody)

        return is_loop, data


class FundHistoryParser(ShareTableParser):

    def parse_item(self, tds):
        return FundJournalData(self.generator.extra['code'], tds[0].string,
                               tds[1].string, tds[3].string)