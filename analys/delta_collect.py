# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
# compute delta of each stock with last 22 days, 14 days, and 7 days
#
#
__author__ = 'keping.chu'


from public.utils import tools

from pyspark import SparkContext
from pyspark.sql import HiveContext, Row, SQLContext
from pyspark.mllib.regression import LabeledPoint, LinearRegressionWithSGD
import sys
reload(sys)
sys.setdefaultencoding('utf8')

select_stock = "select split(rowkey, '_')[0] as date, code, price from hbase_stock where split(rowkey, '_')[0] > '{0}'"

sc = SparkContext(appName='delta collect')
sqlContext = HiveContext(sc)


def convert_to_point(data):
    #rows = [row for row in data[1]]
    sorted_list = sorted(data[1], cmp=lambda frist, second: cmp(frist.date, second.date))

    point_list = []
    for row in sorted_list:
        point_list.append(LabeledPoint(sorted_list.index(row) + 1, [row.price]))

    model = LinearRegressionWithSGD.train(sc.parallelize(each_stock[1]))

    return (data[0], model)


if __name__ == "__main__":

    # data since month ago
    for day in [-30]:
        stocks = sqlContext.sql(select_stock.format(tools.day_after_now(day))).map(lambda row: (row.code, row)).groupByKey().map(convert_to_point)
        for each_stock in stocks.collect():
            print each_stock[0], each_stock[1].weights