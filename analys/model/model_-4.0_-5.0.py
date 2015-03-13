# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'


from pyspark import SparkContext
from analys.model.analys_model import analys
if __name__ == "__main__":
    am = analys(-4.0, -5.0)
    am.process()

