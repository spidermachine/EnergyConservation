# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'

from spider.framework.browser import JSDataGenerator
from spider.extension.hbase import HBaseStorage
from spider.framework.workers import BasicWorker
from spider.framework.parser import Parser


class WorkerFactory(object):

    @staticmethod
    def createBasicWorker(extra):
        """
        basic worker
        """
        data_generator = JSDataGenerator(extra)
        parser = Parser()
        storage = HBaseStorage()
        return BasicWorker(data_generator, storage, parser)