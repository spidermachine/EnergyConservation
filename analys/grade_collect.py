# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'

from pyspark import SparkContext
from pyspark.sql import HiveContext
import sys
reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == "__main__":
    sc = SparkContext(appName='shareDecrease')
    sqlContext = HiveContext(sc)

    stocks = sqlContext.sql("select code, master, grade from hbase_stock_new_grade").filter(lambda row:  row.grade == u'买入').map(lambda row: (row.code, row)).groupByKey().map(lambda row: (row[0], len(row[1]))).sortBy(lambda row: row[1]).collect()

    # print len(stocks)

    for stock in stocks:
        print stock[0], stock[1]
        #     print item.code, item.name, item.delta_ratio
        #     break
        # for item in stock[1]:

    print len(stocks)
