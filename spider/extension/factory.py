# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'cping.ju'

from spider.framework.browser import JSDataGenerator
from spider.framework.storage import HBaseStorage
from spider.framework.workers import BasicWorker
from spider.framework.parser import Parser

class WorkerFactory(object):

    @staticmethod
    def createBasicWorker(self, extra):
        """
        basic worker
        """
        data_generator = JSDataGenerator(extra)
        parser = Parser()
        storage = HBaseStorage()
        return BasicWorker(data_generator, storage, parser)