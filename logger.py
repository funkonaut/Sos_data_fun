"""
Logger logs info to std.out and errors to errors.log
"""

#perhaps should implement different file handlers for each module
#so different log files for errors?
import sys
import logging


class log_filter(object):
    def __init__(self, level):
        self.__level = level

    def filter(self, logRecord):
        return logRecord.levelno <= self.__level


logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s',
                              datefmt='%a, %d %b %Y %H:%M:%S')

sh = logging.StreamHandler(sys.stdout)
sh.setFormatter(formatter)
sh.setLevel(logging.INFO)
sh.addFilter(log_filter(logging.INFO))

fh = logging.FileHandler(filename='errors.log')
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)

logger.addHandler(fh)
logger.addHandler(sh)
