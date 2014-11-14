# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'cping.ju'

from spider.framework.storage import HBaseStorage
from spider.framework.workers import BasicWorker

from spider.extension.yjl.extension import YJLBodyDataGenerator, YJLParser
from spider.extension.industry.extension import Industry, IndustryParser
class WorkerFacade(object):

    @staticmethod
    def process_yjl_worker(extra):
        """
        basic worker
        """
        data_generator = YJLBodyDataGenerator(extra)
        parser = YJLParser()
        storage = HBaseStorage()
        BasicWorker(data_generator, storage, parser).process()

    @staticmethod
    def process_industry_worker(extra):

        data_generator = Industry(extra)
        parser = IndustryParser()
        storage = HBaseStorage()
        BasicWorker(data_generator, storage, parser).process()
