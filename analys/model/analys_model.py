# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'


from public.utils import tools
from pyspark import SparkContext
from pyspark.sql import HiveContext
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class analys(object):

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.name = "model_{0}_{1}".format(str(self.start), str(self.end))

    def two_decreace(self, data):

        first = False
        first_delta = 0.0
        avg = 0.0
        delta = 0.0
        name = None
        category = None
        for row in data[1]:
            delta = float(row.delta_ratio.strip('%'))
            name = row.name
            category = row.category
            # decrease
            if delta <= 0.0:
                # second decrease
                if first:
                    #compute the average
                    avg = (first_delta + delta) / 2
                    return (data[0], name, first_delta, delta, avg, float(row.price)*(100-abs(avg))/100, category)
                else:
                    first_delta = delta
                    first = True
            else:
                first = False

        return (data[0],None, None, None, None)

    def last_days(self):
        import datetime
        day = datetime.datetime.today().weekday()
        if day == 0:
            return -4
        return -3


    def process(self):
        sc = SparkContext(appName=self.name) 
        sqlContext = HiveContext(sc)
        stocks = sqlContext.sql("select split(rowkey, '_')[1] as date, code, name, price, delta_ratio, delta, start, last, height, low, category from hbase_stock where split(rowkey, '_')[1] > '{0}'".format(tools.day_after_now(self.last_days())))\
        .map(lambda row: (row.code, row))\
        .groupByKey().map(self.two_decreace).filter(lambda row: row[1] is not None and row[4] <= self.start and row[4] >= self.end) 
        stock_list = stocks.collect()
        for stock in stock_list:
             print stock[0], stock[1], stock[2], stock[3], stock[4], stock[5], stock[6]
        print len(stock_list)
