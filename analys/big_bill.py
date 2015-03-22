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


def convert(data):

    units = u'万'.encode('utf8').strip()
    volume = data.volume.encode('utf8').strip()
    if units in volume:
        volume = int(float(volume.strip(units)) * 10000)
    else:
        volume = int(float(volume))

    if data.buy_or_sales.encode('utf8') == u'卖盘'.encode('utf8').strip():
        volume = -volume

    print volume

    return (data.code, volume)



if __name__ == "__main__":
    sc = SparkContext(appName='shareDecrease')
    sqlContext = HiveContext(sc)
    bills = sqlContext.sql("select * from hbase_big_bill where date = '{0}'".format('2015-03-20'))\
        .map(convert).reduceByKey(lambda x, y: x + y).sortBy(lambda row: row[1]).collect()

    for bill in bills:
        print bill[0], bill[1]
