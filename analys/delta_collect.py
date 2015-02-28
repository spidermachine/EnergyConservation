# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
# compute delta of each stock with last 22 days, 14 days, and 7 days
#
#
__author__ = 'keping.chu'


from public.utils import tools

from pyspark import SparkContext
from pyspark.sql import HiveContext
from pyspark.mllib.regression import LabeledPoint, LinearRegressionWithSGD
from operator import attrgetter
import sys
reload(sys)
sys.setdefaultencoding('utf8')

select_stock = "select split(rowkey, '_')[1] as date, code, price from hbase_stock where split(rowkey, '_')[1] > '{0}'"


def convert_to_point(data):
    #rows = [row for row in data[1]]
    # sorted_list = sorted(data[1], cmp=lambda first, second: cmp(first.date, second.date))
    sorted_list = sorted(data[1],  key=attrgetter('date'))

    point_list = []
    for row in sorted_list:
        point_list.append(LabeledPoint(float(row.price), [sorted_list.index(row) + 1]))

    return (data[0], sorted_list, point_list)

if __name__ == "__main__":
    sc = SparkContext(appName='delta collect')
    sqlContext = HiveContext(sc)
    # data since month ago
    for day in [-30]:
        stocks = sqlContext.sql(select_stock.format(tools.day_after_now(day))).map(lambda row: (row.code, row)).groupByKey().map(convert_to_point)
        deltas = []
        for each_stock in stocks.collect():
            data_set = sc.parallelize(each_stock[2])
            model = LinearRegressionWithSGD.train(data_set)

            deltas.append((each_stock, model))

        for delta in deltas:
            print delta[0][0],delta[0][1], delta[0][2], delta[1].weights