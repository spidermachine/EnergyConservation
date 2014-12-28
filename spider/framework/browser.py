# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'cping.ju'

import sys, time

reload(sys)
sys.setdefaultencoding('utf-8')

from spynner import browser
from PyQt4.QtWebKit import QWebSettings

class DataGenerator(object):
    """

    """
    def data(self):
        """
        return tuple, (True/False, data), iterate when true, stopped if false
        """
        return False, None


class JSDataGenerator(DataGenerator):

    """
    using spynner to load data
    """

    def __init__(self, extra):
        self.browser = browser.Browser()
        self.browser.set_web_settings(QWebSettings.AutoLoadImages, False)
        self.browser.load_js()
        self.extra = extra
        # show browser if True
        if self.extra.get('show', False):
            self.browser.show()
        self.is_load = self.browser.load(self.extra['url'], load_timeout=self.extra['timeout'])

    def data(self):

        if self.is_load:
            html = unicode(self.browser.webframe.toHtml())
            # print html
            self.is_load = False
            return True, html
        else:
            return False, None


class NextPageDataGenerator(JSDataGenerator):

    def __init__(self, extra):
        super(NextPageDataGenerator, self).__init__(extra)
        self.__first_load = True

    def data(self):
        # the first load
        if self.__first_load:
            self.__first_load = False
        else:
            # collection data of the next page if continue is True, or else do nothing
            if self.extra.get('continue', False):
                self.load_next_page()

        return super(NextPageDataGenerator, self).data()

    def load_next_page(self):

        self.is_load = False
        # sleep 3 seconds, if no command
        sleep = self.extra.get('sleep', 3)
        time.sleep(sleep)

        # find link of next page
        web_elements = self.browser.webframe.findAllElements(self.extra['tag'])
        for element in web_elements:
            # found the next page
            if str(element.toInnerXml()).strip() == self.extra['text']:
                # trigger the link and load the next page
                element.evaluateJavaScript("this.onclick()")
                self.browser.wait_load(timeout=self.extra['timeout'])
                self.is_load = True
                break
