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
    sc = SparkContext(appName='shareDecrease')
    sqlContext = HiveContext(sc)
    otherContext = SQLContext(sc)
    stocks = sqlContext.sql("select split(rowkey, '_')[0] as date, code, price from hbase_stock where date > '{0}' ".format()).map(lambda row: (row.code, row)).groupByKey().filter(two_decreace).map(sum_decrease_info).filter(lambda row: row[1] <= -0.0).map(lambda row: Row(code=row[0], delta=row[1]))
    stocksSchema = otherContext.inferSchema(stocks)
    stocksSchema.registerTempTable("stocks")
    fund = sqlContext.sql("select * from hbase_fund_share").map(lambda row: (row.code, row)).groupByKey().map(lambda row: Row(code=row[0], weight=len(row[1])))
    fundSchema = otherContext.inferSchema(fund)
    fundSchema.registerTempTable("fund")
    items = otherContext.sql("select g.code, g.name, g.grade, s.delta, f.weight from grade g, stocks s, fund f where g.code=s.code and g.code=f.code").collect()

    print len(items)
    for item in items:
        print item.code, item.name, item.grade, item.delta, item.weight
