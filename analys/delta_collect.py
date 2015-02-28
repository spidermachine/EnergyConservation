# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
# compute delta of each stock with last 22 days, 14 days, and 7 days
#
#
__author__ = 'keping.chu'


from public.utils import tools

from pyspark import SparkContext
from pyspark.sql import HiveContext, Row, SQLContext
from pyspark.mllib.regression import LabeledPoint, LinearRegressionWithSGD
import sys
reload(sys)
sys.setdefaultencoding('utf8')

select_stock = "select split(rowkey, '_')[0] as date, code, price from hbase_stock where split(rowkey, '_')[0] > '{0}'"

def sum_decrease_info(data):

    sum_decreace = 0.0
    for row in data[1]:
        sum_decreace += float(row.delta_ratio.strip('%'))

    return (data[0], sum_decreace)

def convert_to_point(data):

	#rows = [row for row in data[1]]
	sorted_list = sorted(data[1], cmp=lambda frist, second: cmp(frist.date, second.date))
	index = 1
	point_list = []#[LabeledPoint(index=index+1, [row.price]) for row in sorted_list]
	for row in sorted_list:
		point_list.append(LabeledPoint(sorted_list.index(row), [row.price])) 
	#return (data[0], sorted(data[1], cmp=lambda frist, second: cmp(frist.date, second.date)))
	return (data[0], data[1], point_list)
	
if __name__ == "__main__":
    sc = SparkContext(appName='delta collect')
    sqlContext = HiveContext(sc)
    otherContext = SQLContext(sc)
	# data since month ago
    for day in [-30]:
		stocks = sqlContext.sql(select_stock.format(tools.day_after_now(day))).map(lambda row: (row.code, row)).groupByKey().map(convert_to_point)
		for each_stock in stocks.collect():
			data_set = sc.parallelize(each_stock[2])
			model = LinearRegressionWithSGD.train(data_set)
			print dir(model)
