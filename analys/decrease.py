# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'

from pyspark import SparkContext
from pyspark.sql import HiveContext


if __name__ == "__main__":
    sc = SparkContext(appName='continueDecrease')
    sqlContext = HiveContext(sc)

    stocks = sqlContext.sql("select key, code from hbase_stock")

    for stock in stocks:
        print stock
