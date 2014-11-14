# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'cping.ju'


from spider.framework.browser import JSDataGenerator
from spider.framework.parser import Parser
from . import tags

from bs4 import BeautifulSoup



class TableDataGenerator(JSDataGenerator):

    def __init__(self, extra):
        super(TableDataGenerator, self).__init__(extra)
        self.class_ = ""

    def data(self):

        is_loop, data = super(TableDataGenerator, self).data()
        if data:
            soup = BeautifulSoup(data, from_encoding='uft-8')
            data = soup.find(tags.table, class_=self.class_)
            data = str(data)
        return is_loop, data


class TableBodyDataGenerator(TableDataGenerator):

    def __init__(self, extra):
        super(TableBodyDataGenerator, self).__init__(extra)

    def data(self):

        is_loop, data = super(TableBodyDataGenerator, self).data()
        if data:
            soup = BeautifulSoup(data, from_encoding='uft-8')
            data = soup.find(tags.table, class_=self.class_)
            data = str(data.find(tags.tbody))
        return is_loop, data


class TableParser(Parser):

    def parse(self, string):
        items = []
        soup = BeautifulSoup(string, from_encoding="utf-8")
        for tr in soup.find_all(tags.tr):
            tds = tr.find_all(tags.td)
            items.append(self.parse(tds))

        return items

    def parse_item(self, tds):
        pass
