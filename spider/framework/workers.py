# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'cping.ju'


class BasicWorker(object):
    """
    in this worker, the following things done:
    1. load data from internet.
    2. parse interest fragment.
    3. save data.
    """
    def __init__(self, data_generator=None, storage=None, parser=None):
        self.data_generator = data_generator
        self.storage = storage
        self.parser = parser

    def process(self):
        """
        load data from internet, extract data, and then save data
        """

        while True:
            is_loop, data = self.data_generator.data()
            if data:
                self.save(self.parse(data))

            if not is_loop:
                break

    def parse(self, data):
        """
        parse data
        """
        if self.parser:
            return self.parser.parse(data)
        return data

    def save(self, data):
        """
        save data
        """
        if self.storage:
            if isinstance(data, list):
                self.storage.batch_save(data)
            else:
                self.storage.save(data)