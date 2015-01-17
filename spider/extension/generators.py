# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'


from spider.framework.browser import NextPageDataGenerator
from spider.framework.parser import Parser
from . import tags

from bs4 import BeautifulSoup


class TableDataGenerator(NextPageDataGenerator):

    def __init__(self, extra):
        super(TableDataGenerator, self).__init__(extra)

    def data(self):

        is_loop, data = super(TableDataGenerator, self).data()
        if data:
            soup = BeautifulSoup(data, from_encoding='uft-8')
            if self.extra.get("id", None):
                data = soup.find(tags.table, id=self.extra['id'])
            elif self.extra.get("class", None):
                data = soup.find(tags.table, class_=self.extra['class'])

            data = str(data)
        return is_loop, data


class TableBodyDataGenerator(TableDataGenerator):

    def __init__(self, extra):
        super(TableBodyDataGenerator, self).__init__(extra)

    def data(self):

        is_loop, data = super(TableBodyDataGenerator, self).data()
        if data:
            soup = BeautifulSoup(data, from_encoding='uft-8')
            data = str(soup.find(tags.tbody))
        return is_loop, data


class TableParser(Parser):

    def parse(self, string, generator=None):
        items = []
        soup = BeautifulSoup(string, from_encoding="utf-8")
        for tr in soup.find_all(tags.tr):
            tds = tr.find_all(tags.td)
            item = self.parse_item(tds)
            if item:
                items.append(item)

        return items

    def parse_item(self, tds):
        pass

    def parse_tag_a(self, td):

        a = td.find("a")
        if a:
            return a.string, a['href']

        return None, None