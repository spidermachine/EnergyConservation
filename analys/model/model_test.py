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
    if (1-float(row.low)/float(row.last))*100 >= avg:
        return row.delta_ratio
    else:
        return 100


def sales(row, avg):

    if float(row.height)/float(row.last)*100 - 1 >= abs(avg):
        return row.delta_ratio
    else:
        return float(row.delta)/float(row.last)*100


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
            result.append((buydata[0], buydata[1], sales(row, buydata[0])))
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
    stocks = sqlContext.sql("select split(rowkey, '_')[0] as date, code, name, price, delta_ratio, delta, start, last, height, low from hbase_stock where code = '601111'")\
        .map(lambda row: (row.code, row))\
        .groupByKey().map(two_decreace).filter(lambda row: len(row[1]) > 0)

    stocks = stocks.collect()
    for stock in stocks:
        print stock[0], stock[1]
    print len(stocks)
