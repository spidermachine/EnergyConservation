# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'cping.ju'

from spider.framework.storage import HBaseStorage
from spider.framework.workers import BasicWorker

from spider.extension.yjl.extension import YJLBodyDataGenerator, YJLParser
from spider.extension.industry.extension import Industry, IndustryParser
from spider.extension.share.extension import ShareTableParser, ShareDataGenerator
from spider.extension.fund.extension import FundBodyDataGenerator, FundHistoryDataGenerator, FundJournalGenerator, \
    FundHistoryParser, FundJournalParser, FundParser

class WorkerFacade(object):

    @staticmethod
    def worker(generator, parser):
        """
        basic worker
        """
        storage = HBaseStorage()
        BasicWorker(generator, storage, parser).process()

    @staticmethod
    def process_yjl(extra):
        """
        yjl worker
        """
        data_generator = YJLBodyDataGenerator(extra)
        parser = YJLParser()
        WorkerFacade.worker(data_generator, parser)

    @staticmethod
    def process_industry(extra):
        """
        industry money flow
        """
        data_generator = Industry(extra)
        parser = IndustryParser()
        WorkerFacade.worker(data_generator, parser)

    @staticmethod
    def process_share(extra):
        """
        share holds
        """
        data_generator = ShareDataGenerator(extra)
        parser = ShareTableParser()
        WorkerFacade.worker(data_generator, parser)

    @staticmethod
    def process_fund_list(extra):
        """
        fund list
        """
        data_generator = FundBodyDataGenerator(extra)
        parser = FundParser()
        WorkerFacade.worker(data_generator, parser)

    @staticmethod
    def process_fund_history(extra):
        """
        history price of fund
        """
        data_generator = FundHistoryParser(extra)
        parser = FundHistoryParser()
        WorkerFacade.worker(data_generator, parser)

    @staticmethod
    def process_fund_journal(extra):
        """
        lasted fund price
        """
        data_generator = FundJournalGenerator(extra)
        parser = FundJournalParser()
        WorkerFacade.worker(data_generator, parser)


