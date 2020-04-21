#!/usr/bin/python3
# _*_ coding:UTF-8 _*_


import logging.handlers
import multiprocessing
import os
import re
import time
import datetime
from logging.handlers import TimedRotatingFileHandler,RotatingFileHandler

from config import config

# 配置：
LOG_LEVEL = logging.INFO
LOG_NAME = 'root'
IS_MULTIPROCESS = False
IS_BACKGROUND = False

LOGFILE_PATH = config.logfile_path

# 取得日志保存的路径，可直接建立多级目录
if not os.path.exists(LOGFILE_PATH):
    os.makedirs(LOGFILE_PATH)


class SafeTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, *args, **kwargs):
        super(SafeTimedRotatingFileHandler, self).__init__(*args, **kwargs)
        self.suffix_time = ""
        self.origin_basename = self.baseFilename

    def shouldRollover(self, record):
        timeTuple = time.localtime()
        if self.suffix_time != time.strftime(self.suffix, timeTuple) or not os.path.exists(
                self.origin_basename + '.' + self.suffix_time):
            return 1
        else:
            return 0

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None

        currentTimeTuple = time.localtime()
        self.suffix_time = time.strftime(self.suffix, currentTimeTuple)
        self.baseFilename = self.origin_basename + '.' + self.suffix_time

        self.mode = 'a'

        global lock
        with lock:
            if self.backupCount > 0:
                for s in self.getFilesToDelete():
                    os.remove(s)

        if not self.delay:
            self.stream = self._open()

    def getFilesToDelete(self):
        # 将源代码的 self.baseFilename 改为 self.origin_basename
        dirName, baseName = os.path.split(self.origin_basename)
        fileNames = os.listdir(dirName)
        result = []
        prefix = baseName + "."
        plen = len(prefix)
        for fileName in fileNames:
            if fileName[:plen] == prefix:
                suffix = fileName[plen:]
                if self.extMatch.match(suffix):
                    result.append(os.path.join(dirName, fileName))
        if len(result) < self.backupCount:
            result = []
        else:
            result.sort()
            result = result[:len(result) - self.backupCount]
        return result

log_filename = LOGFILE_PATH + LOG_NAME  # 统一日志文件名称格式
if IS_BACKGROUND and IS_MULTIPROCESS:
    log_filename = log_filename + '.{}.pid'.format(os.getpid())
    # 多进程日志调度：
    lock = multiprocessing.Lock()
    # 多进程日志安全分割实现
    handler = SafeTimedRotatingFileHandler(log_filename, when='D', interval=1, backupCount=180, encoding='utf-8')
    # 日志分割的后缀格式
    handler.suffix = '%Y-%m-%d.log'
    handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")

elif IS_BACKGROUND and not IS_MULTIPROCESS:
    log_filename = log_filename  # 用定时任务启动脚本时，统一日志文件名称格式
    handler = TimedRotatingFileHandler(log_filename, when='D', interval=1, backupCount=180, encoding='utf-8')
    handler.suffix = '%Y-%m-%d.log'
    handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")

else:
    log_filename = log_filename + '.{}.log'.format(datetime.datetime.today().date())
    handler = RotatingFileHandler(log_filename, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8')
# 消息格式字符串和日期字符串
fmt = '%(asctime)s %(filename)s %(lineno)d行(%(funcName)s方法):%(name)s/进程%(process)d/线程%(thread)d(%(threadName)s)):' \
      ' %(levelname)s   %(message)s'
date_fmt = '%Y-%m-%d %A %H:%M:%S'
handler.setFormatter(logging.Formatter(fmt, date_fmt))
logger = logging.getLogger(LOG_NAME)
logger.setLevel(LOG_LEVEL)
logger.addHandler(handler)
