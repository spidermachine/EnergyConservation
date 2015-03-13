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
    delta = 0.0
    name = None
    for row in data[1]:
        delta = float(row.delta_ratio.strip('%'))
        name = row.name
        # decrease
        if delta <= 0.0:
            # second decrease
            if first:
                #compute the average
                avg = (first_delta + delta) / 2
                return (data[0], name, first_delta, delta, avg, float(row.price)*(100-abs(avg))/100)
            else:
                first_delta = delta
                first = True
        else:
            first = False

    return (data[0],None, None, None, None)

def last_days():
    import datetime
    day = datetime.datetime.today().weekday()
    if day == 0:
        return -4
    return -4

if __name__ == "__main__":
    sc = SparkContext(appName='model_one')
    sqlContext = HiveContext(sc)
    otherContext = SQLContext(sc)
    stocks = sqlContext.sql("select split(rowkey, '_')[1] as date, code, name, price, delta_ratio, delta, start, last, height, low from hbase_stock where split(rowkey, '_')[1] > '{0}'".format(tools.day_after_now(last_days())))\
        .map(lambda row: (row.code, row))\
        .groupByKey().map(two_decreace).filter(lambda row: row[1] is not None)

    stocks = stocks.collect()
    for stock in stocks:
        print stock[0], stock[1], stock[2], stock[3], stock[4], stock[5]
    print len(stocks)
