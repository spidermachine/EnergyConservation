# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'

from spider.extension.hbase import ThriftHBaseStorage, HBaseStorage
from spider.framework.workers import BasicWorker

from spider.extension.generators import TableBodyDataGenerator
from spider.extension.stock.extension import StockDataGenerator, StockTableParser, StockGradeParser, StockAparser
from spider.extension.grade.extendsion import GradeDataParser
from spider.extension.yjl.extension import YJLParser
from spider.extension.industry.extension import IndustryParser
from spider.extension.share.extension import ShareTableParser, ShareDataGenerator
from spider.extension.fund.extension import FundRetParser, FundRetGenerator, FundParser, FundBodyDataGenerator

from public.utils import tables, memcache

# from celery.utils.log import get_task_logger
#
# logger = get_task_logger(__name__)


class WorkerFacade(object):

    @staticmethod
    def worker(generator, parser):
        """
        basic worker
        """

        # BasicWorker(generator, ThriftHBaseStorage.get_instance(), parser).process()
        BasicWorker(generator, HBaseStorage(), parser).process()

    @staticmethod
    def process_yjl(extra):
        """
        yjl worker
        """
        data_generator = TableBodyDataGenerator(extra)
        parser = YJLParser()
        WorkerFacade.worker(data_generator, parser)

    @staticmethod
    def process_industry(extra):
        """
        industry money flow
        """
        data_generator = TableBodyDataGenerator(extra)
        parser = IndustryParser()
        WorkerFacade.worker(data_generator, parser)

    @staticmethod
    def process_share(extra):
        """
        share holds
        """
        columns = ["{0}:{1}".format(tables.COLUMN_FAMILY, tables.CODE),
                   "{0}:{1}".format(tables.COLUMN_FAMILY, tables.URL),
                   "{0}:{1}".format(tables.COLUMN_FAMILY, tables.TABLE_VISITED)]


        rows = ThriftHBaseStorage.get_instance().fetch(tables.TABLE_FUND, tables.TABLE_VISITED, memcache.get_visited(),
                                                       '=', columns)
        # logger.debug(rows)
        if not rows:
            memcache.set_reverse()
            rows = ThriftHBaseStorage.get_instance().fetch(tables.TABLE_FUND, tables.TABLE_VISITED, memcache.get_visited(),
                                                           '=', columns)
        # logger.debug(rows)
        if rows:
            extra['fund'] = rows[0].columns.get(columns[0]).value
            extra['url'] = rows[0].columns.get(columns[1]).value
            data_generator = ShareDataGenerator(extra)
            parser = ShareTableParser()
            # logger.debug("worker start")
            WorkerFacade.worker(data_generator, parser)
            # logger.debug("worker end")
            ThriftHBaseStorage.get_instance().update(tables.TABLE_FUND, rows[0].row, {memcache.visited: memcache.unvisited if memcache.get_visited() == memcache.visited else memcache.visited})

    @staticmethod
    def process_fund_list(extra):
        """
        fund list
        """
        data_generator = FundBodyDataGenerator(extra)
        parser = FundParser()
        WorkerFacade.worker(data_generator, parser)

    @staticmethod
    def process_fund_grade(extra):
        """
        grade
        """
        data_generator = TableBodyDataGenerator(extra)
        parser = GradeDataParser()
        WorkerFacade.worker(data_generator, parser)

    @staticmethod
    def process_stock(extra):
        """
        grade
        """
        data_generator = StockDataGenerator(extra)
        parser = StockTableParser()
        WorkerFacade.worker(data_generator, parser)

    @staticmethod
    def process_fund_return(extra):
        """
        return of fund
        """
        data_generator = FundRetGenerator(extra)
        parser = FundRetParser()
        WorkerFacade.worker(data_generator, parser)

    @staticmethod
    def process_stock_grade(extra):
        """
        stock's grade
        """
        data_generator = TableBodyDataGenerator(extra)
        parser = StockGradeParser()
        WorkerFacade.worker(data_generator, parser)

    @staticmethod
    def process_a_stock(extra):
        data_generator = StockDataGenerator(extra)
        parser = StockAparser()
        WorkerFacade.worker(data_generator, parser)