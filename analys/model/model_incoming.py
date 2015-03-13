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

    if (float(row.height)/float(row.last) - 1)*100 >= abs(avg):
        return (row.delta_ratio, row.height, row.last)
    else:
        return ((float(row.height)/float(row.last) -1)*100, row.height, row.last)


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
                if avg >= -2.0:
                    avg = 0.0
            first_delta = delta
            first = True
        else:
            first_delta = 0.0
            avg = 0.0
            first = False

    return (data[0], result)

def buy_sales_ratio(data):

    pass

def sales_ratio(data):

    result = data[1]
    sales = 0
    unsales = 0
    for item in result:
        if len(item) == 3:
            print '---------------------', item, type(item[2][0])
            if type(item[2][0]) is unicode:
                sales += 1
            else:
                unsales +=1
    return (data[0], sales, unsales)

def incoming_ratio(data):

    result = data[1]
    sales = 0
    unsales = 0
    for item in result:
        if len(item) == 3:
            print '---------------------', item, type(item[2][0])
            if type(item[2][0]) is unicode:
                sales += 1
            elif item[2][0] <= 0:
                unsales +=1
            else:
                sales +=1
    return (data[0], sales, unsales)


if __name__ == "__main__":
    sc = SparkContext(appName='model_one')
    sqlContext = HiveContext(sc)
    otherContext = SQLContext(sc)
    stocks = sqlContext.sql("select split(rowkey, '_')[0] as date, code, name, price, delta_ratio, delta, start, last, height, low from hbase_stock")\
        .map(lambda row: (row.code, row))\
        .groupByKey()\
        .map(two_decreace)\
        .filter(lambda row: len(row[1]) > 0)\
        .map(incoming_ratio)\
        .reduce(lambda first, second: (None, first[1] + second[1], first[2] + second[2]))
    print stocks
    print (float(stocks[1])/float(stocks[2]+stocks[1]), float(stocks[2])/float(stocks[1]+stocks[2]))

#stocks = stocks.collect()
#    for stock in stocks:
#        print stock[0], stock[1]
#    print len(stocks)
