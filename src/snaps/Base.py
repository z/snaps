import logging

from .Config import Config


class Base(object):

    def __init__(self):
        self.config = Config.get_instance().config
        self.log = logging.getLogger('.'.join([self.__module__, self.__class__.__name__]))
        self.log.setLevel(level=self.config['default']['log_level'])
