# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'


from public.utils import tools

from pyspark import SparkContext
from pyspark.sql import HiveContext, Row, SQLContext
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def buy(row, avg):

    if float(row.low)/float(row.last) <= avg:
        return float(row.delta_ratio.strip('%'))
    else:
        return 100


def sales(row, avg):

    if float(row.delta)/float(row.last) >= abs(avg):
        return row.delta_ratio.strip('%')
    else:
        return float(row.delta)/float(row.last)


def two_decreace(data):

    first = False
    first_delta = 0.0
    avg = 0.0
    result = []
    sale = False
    for row in data[1]:
        # sale
        if sale:
            buydata = result.pop()
            result.append((buydata[0], buydata[1], sales(row)))
            sale = False

        # buy
        if avg < 0.0:
            tmp = buy(row, avg)
            if tmp != 100:
                result.append((avg, tmp))
                sale = True
            avg = 0.0

        delta = float(row.delta_ratio.strip('%'))
        # decrease
        if delta < 0.0:
            # second decrease
            if first:
                #compute the average
                avg = (first_delta + delta) / 2
            first_delta = delta
            first = True
        else:
            first_delta = 0.0
            avg = 0.0
            first = False

    return (data[0], result)


if __name__ == "__main__":
    sc = SparkContext(appName='model_one')
    sqlContext = HiveContext(sc)
    otherContext = SQLContext(sc)
    stocks = sqlContext.sql("select split(rowkey, '_')[0] as date, code, name, price, delta_ratio, start, last, height, low from hbase_stock ")\
        .map(lambda row: (row.code, row))\
        .groupByKey().map(two_decreace).filter(lambda row: len(row[1]) > 0)

    for stock in stocks.collect():
        print stock[0], stock[1]
