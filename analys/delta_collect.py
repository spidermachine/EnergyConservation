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
from operator import attrgetter
from sklearn import linear_model

import sys
reload(sys)
sys.setdefaultencoding('utf8')

select_stock = "select split(rowkey, '_')[1] as date, code, delta_ratio from hbase_stock where split(rowkey, '_')[1] > '{0}'"


def convert_to_point(data):
    #rows = [row for row in data[1]]
    # sorted_list = sorted(data[1], cmp=lambda first, second: cmp(first.date, second.date))
    sorted_list = sorted(data[1],  key=attrgetter('date'))

    features = []
    labels = []
    for row in sorted_list:
        labels.append(float(row.delta_ratio.strip('%')))
        features.append([sorted_list.index(row) + 1])

    clf = linear_model.LinearRegression()
    clf.fit(features, labels)

    return (data[0], sorted_list, clf.coef_, clf.intercept_)

if __name__ == "__main__":
    sc = SparkContext(appName='delta collect')
    sqlContext = HiveContext(sc)
    # data since month ago
    for day in [-30]:
        stocks = sqlContext.sql(select_stock.format(tools.day_after_now(day))).map(lambda row: (row.code, row)).groupByKey().map(convert_to_point).sortBy(lambda row: row[2][0])

        for each_stock in stocks.collect():
            print each_stock[0], each_stock[1], each_stock[2], each_stock[3]