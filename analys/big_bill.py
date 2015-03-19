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


def convert(data):

    if data.buy_or_sales == u'买盘':
        volume = int(data.volume)
    else:
        volume = -int(data.volume)

    return (data.code, volume)

#
# def sum_data(data):
#
#     for row in data[1]:
#
#         if float(row.delta_ratio.strip('%')) > 0.0:
#             return False
#
#     if len(data[1]) == 0:
#         return False
#
#     return True


if __name__ == "__main__":
    sc = SparkContext(appName='shareDecrease')
    sqlContext = HiveContext(sc)
    bills = sqlContext.sql("select * from hbase_big_bill where date = '{0}'".format(tools.current_date()))\
        .map(convert).reduceByKey(lambda x, y: x + y).collect()

    for bill in bills:
        print bill[0], bill[1]