# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'cping.ju'

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from spynner import browser
from PyQt4.QtWebKit import QWebSettings

class DataGenerator(object):
    """

    """
    def load_url(self, url):
        pass

    def data(self):
        """
        return tuple, (True/False, data), iterate when true, stopped if false
        """
        return False, None


class JSDataGenerator(DataGenerator):

    """
    using spynner to load data
    """

    def __init__(self):
        self.browser = browser.Browser()
        self.browser.set_web_settings(QWebSettings.AutoLoadImages, False)
        self.browser.load_js()
        self.is_load = False

    def load_url(self, url):

        try:
            self.is_load = self.browser.load(url, load_timeout=600)
            return self.is_load
        except:
            return False

    def data(self):

        if self.is_load:
            html = unicode(self.browser.webframe.toHtml())
            return True, html
        else:
            return False, None


class NextPageDataGenerator(JSDataGenerator):

    def __init__(self):
        super(NextPageDataGenerator, self).__init__()
        self.__first_load = False

    def load_url(self, url):

        self.__first_load = True
        return super(NextPageDataGenerator, self).load_url(url)

    def data(self):

        if self.__first_load:
            self.__first_load = False
        else:
            self.load_next_page()

        return super(NextPageDataGenerator, self).data()

    def load_next_page(self):
        self.is_load = False