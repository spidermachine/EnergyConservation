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


def sum_decrease_info(data):

    sum_decreace = 0.0
    for row in data[1]:
        sum_decreace += float(row.delta_ratio.strip('%'))

    return (data[0], sum_decreace)

def two_decreace(data):

    for row in data[1]:

        if float(row.delta_ratio.strip('%')) > 0.0:
            return False

    if len(data[1]) == 0:
        return False

    return True

if __name__ == "__main__":
    sc = SparkContext(appName='continueDecrease')
    sqlContext = HiveContext(sc)

    stocks = sqlContext.sql("select * from hbase_stock where split(rowkey, '_')[1] > '{0}'".format(tools.day_after_now(-2))).map(lambda row: (row.code, row)).groupByKey().filter(two_decreace).map(sum_decrease_info).filter(lambda row: row[1] <= -3.0).sortBy(lambda row: row[1]).collect()

    # print len(stocks)
    content = ''
    for stock in stocks:
        print stock[0], stock[1]
        content += stock[0] + ': ' + str(stock[1]) + '\n'
        # for item in stock[1]:
        #     print item.code, item.name, item.delta_ratio
        #     break

    tools.send_mail(u'连跌3天', content, 'energyconversation', 'zkpprivate@163.com')