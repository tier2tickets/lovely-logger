# Copyright 2021 [Tier2 Technologies](https://www.tier2.tech/). All rights reserved.
#
# Distributed under LGPL-2.1 license.
# See file LICENSE for detail or copy at https://opensource.org/licenses/LGPL-2.1

'''
===================================================================================================
This module is a logger library which builds on and combines various logging features of Python 3.
It handles automatic logging of exception tracebacks
It handles simultaneous logging to both stdout (the console) and an automatically rotating file
It simplifies advanced logging techniques such as independent formatters for console vs file
It is robust; thread-safe and able to flush the log on program crash/exit
It has reasonable defaults, and a simple interface
'''
import logging
from logging.handlers import QueueListener, QueueHandler
import logging.handlers
import sys
import atexit
from queue import Queue
from datetime import datetime
import time

DEBUG = logging.DEBUG
WARNING = logging.WARNING
ERROR = logging.WARNING
CRITICAL = logging.CRITICAL

# python's time.strftime() format with an added optional milliseconds - 'uuu'
# 'uuu' added to match the documentation:
# https://docs.python.org/3/library/logging.html#logging.Formatter.formatTime
DATE_FORMAT = '%Y-%m-%d %H:%M:%S.uuu%z'

FILE_FORMAT = "[%(asctime)s] [%(levelname)-8s] - %(message)s (%(filename)s:%(lineno)s)"
CONSOLE_FORMAT = "[%(levelname)-8s] - %(message)s (%(filename)s:%(lineno)s)"

# in a module, __name__ is the module’s name in the Python package name space.
logger = logging.getLogger(__name__)

debug = d = logger.debug
info = i = logger.info
warning = w = logger.warning
error = e = logger.error
critical = c = logger.critical
exception = x = logger.exception

def init(filename, to_console=True, level=DEBUG, max_kb=1024, max_files=5):
    ''' call this function after overriding the format constants to initialize the logger '''
    logger.setLevel(level)

    # overriding the default logging.Formatter because it uses time.strftime,
    # which has no support for milliseconds, and datetime.strftime does
    class CustomFormatter(logging.Formatter):
        ''' overriding the default logging.Formatter because it uses time.strftime
            which has no support for microseconds, and datetime.strftime does
        '''
        def formatTime(self, record, datefmt=None):
            formatted_time = time.strftime(datefmt, self.converter(record.created))
            formatted_time = formatted_time.replace(
                'uuu',
                datetime.fromtimestamp(record.created).strftime('%f')[0:3]
            )
            return formatted_time


    # create a rotating file handler queue
    # (logging queues are needed to prevent deadlocks in threading)
    log_queue = Queue()
    log_file_handler = logging.handlers.RotatingFileHandler(
        filename,
        maxBytes=max_kb*1024,
        backupCount=max_files - 1,
        encoding='utf-8'
    )

    formatter_file = CustomFormatter(fmt=FILE_FORMAT, datefmt=DATE_FORMAT)
    log_file_handler.setFormatter(formatter_file)
    queue_listener = QueueListener(log_queue, log_file_handler)
    queue_listener.start()

    if to_console:
        # create a stream handler which logs to sys.stderr
        log_stream_handler = logging.StreamHandler()
        # create formatter and add it to the handler
        formatter_console = CustomFormatter(CONSOLE_FORMAT, datefmt=DATE_FORMAT)
        log_stream_handler.setFormatter(formatter_console)
        logger.addHandler(log_stream_handler)

    # Push file logs into the queue:
    logger.addHandler(QueueHandler(log_queue))

    # build a handler that can log uncaught exceptions
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.critical("Uncaught Exception:", exc_info=(exc_type, exc_value, exc_traceback))


    # and then we attach that handler to the except hook
    sys.excepthook = handle_exception

    # attach an exit handler so that the program waits for the queue to empty before exiting.
    atexit.register(queue_listener.stop)
