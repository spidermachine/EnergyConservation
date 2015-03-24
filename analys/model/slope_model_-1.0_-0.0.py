# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'

from analys.model.slope_model import SlopeModel

if __name__ == "__main__":

    slope = SlopeModel(start=-1.0, end=-0.0)

    slope.process()