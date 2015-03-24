# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'



from public.utils import tools

from pyspark import SparkContext
from pyspark.sql import HiveContext
from operator import attrgetter
from sklearn import linear_model

import sys
reload(sys)
sys.setdefaultencoding('utf8')

select_stock = """select split(rowkey, '_')[1] as date,
                code, name,
                delta_ratio from hbase_stock
                 where split(rowkey, '_')[1] > '{0}'"""


class SlopeModel(object):

    def __init__(self, days=7, start=-10.0, end=10.0):
        self.days = days
        self.start = start
        self.end = end

    def convert_to_point(data):
        #rows = [row for row in data[1]]
        # sorted_list = sorted(data[1], cmp=lambda first, second: cmp(first.date, second.date))
        sorted_list = sorted(data[1],  key=attrgetter('date'))

        features = []
        lables = []
        sum_amplitude = 0.0
        name = ''
        for row in sorted_list:
            name = row.name
            sum_amplitude += float(row.delta_ratio.strip('%'))
            lables.append(sum_amplitude)
            features.append([sorted_list.index(row) + 1])

        clf = linear_model.LinearRegression()
        clf.fit(features, lables)
        return (data[0], name,  clf.coef_, len(lables))
        #return (data[0], sorted_list, clf.coef_, clf.intercept_)

    def process(self):
        sc = SparkContext(appName='delta collect')
        sqlContext = HiveContext(sc)
        # data since month ago
        stocks = sqlContext.sql(select_stock.format(tools.day_after_now(self.days)))\
            .map(lambda row: (row.code, row))\
            .groupByKey()\
            .map(self.convert_to_point)\
            .filter(lambda row: row[2][0] >= self.start and row[2][0] <= self.end)\
            .sortBy(lambda row: row[2][0])

        for each_stock in stocks.collect():
            print each_stock[0], each_stock[1], each_stock[2], each_stock[3]