# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'cping.ju'


class Manager(object):

    def Manager(self, data_generator=None, storage=None, parser=None, extra={}):
        self.data_generator = data_generator
        self.storage = storage
        self.parser = parser
        self.extra = extra

    def process(self):

        if self.data_generator.load(self.extra['url']):
            while True:
                is_loop, data = self.data_generator.data()
                if data:
                    if self.parser:
                        data = self.parser.parse(data)
                    if self.storage:
                        if isinstance(data, list):
                            self.storage.batch_save(data)
                        else:
                            self.storage.save(data)
                if not is_loop:
                    break