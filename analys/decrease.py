# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'

from pyspark import SparkContext
from pyspark.sql import HiveContext


if __name__ == "__main__":
    sc = SparkContext(appName='continueDecrease')
    sqlContext = HiveContext(sc)

<<<<<<< HEAD
    stocks = sqlContext.sql("select rowkey, code from hbase_stock").collect()
=======
    stocks = sqlContext.sql("select key, code from hbase_stock").collect()
>>>>>>> ff1877a43ca5d2ecb1670434cf50449d0611dfe6

    for stock in stocks:
        print stock
