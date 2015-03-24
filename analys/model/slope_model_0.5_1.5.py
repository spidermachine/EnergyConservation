# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'

from analys.model.slope_model import SlopeModel

if __name__ == "__main__":

    slope = SlopeModel(start=0.5, end=1.5)

    slope.process()