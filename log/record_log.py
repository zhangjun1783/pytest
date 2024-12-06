import logging
import logging.handlers
import logging.config
import os
import sys

"""
读取日志配置文件，并实例化run_log
"""


def record_log():
    filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config/log.ini'))
    logging.config.fileConfig(filename)
    return logging.getLogger()


def close_log():
    return logging.shutdown()
