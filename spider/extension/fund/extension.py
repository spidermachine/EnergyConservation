# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'cping.ju'


from spider.extension.generators import TableParser, TableBodyDataGenerator, TableDataGenerator
from spider.framework.storage import HBaseData
from spider.extension import tags
from public.utils import tables


from bs4 import BeautifulSoup


class FundBodyDataGenerator(TableBodyDataGenerator):

    def __init__(self, extra):

        super(FundBodyDataGenerator, self).__init__(extra)

        self.class_ = "dbtable"


class FundData(HBaseData):

    def __init__(self, code, name, url):
        self.code = code.strip()
        self.name = name.strip()
        self.url = url.strip()

    def row(self):

        return self.code

    def table(self):
        return "fund"

    def columns(self):

        return {"c1": {"code": self.code, "name": self.name, "url": self.url}}


class FundParser(TableParser):

    def parse_item(self, tds):

        a = tds[4].find("a")
        return FundData(tds[3].string, a.string, a["href"])



class FundJournalGenerator(TableDataGenerator):

    def __init__(self, extra):

        super(FundJournalGenerator, self).__init__(extra)

        self.class_ = "dbtable"


class FundJournalData(HBaseData):

    def __init__(self, name, code, date, price, increase, percent):

        self.name = name.strip()
        self.code = code.strip()
        self.date = date.strip()
        self.price = price.strip()
        self.increase = increase.strip()
        self.percent = percent.strip()

    def row(self):

        return tables.ROW_ID.format(self.code, self.date)

    def table(self):

        return "fund_journal"

    def columns(self):

        return {"c1": {"name": self.name, "code": self.code, "date": self.date, "price": self.price,
                       "increase": self.increase, "percent": self.percent}}


class FundJournalParser(TableParser):

    def __init__(self):
        self.date = None

    def parse(self, string):

        soup = BeautifulSoup(string, from_encoding="utf-8")

        self.date = soup.find(tags.thead).find(tags.tr).find_all(tags.td)[6].string.strip()

        return super(FundJournalParser, self).parse(string)



    def parse_item(self, tds):

        a = tds[4].find("a")
        return FundJournalData(a.string, tds[3].string, self.date, tds[7].string, tds[9].string, tds[10].string)
