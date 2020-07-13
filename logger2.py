
import datetime
import logging.handlers
import os
import sys

# 兼容python2
if sys.version[0]=='2':
  reload(sys)
  sys.setdefaultencoding('utf-8')
  
# 配置：
LOG_NAME = 'main'

# 通过日志文件的相对路径得到日志文件的绝对路径
log_path = '{}/../log'.format(os.path.split(os.path.realpath(__file__))[0])
os.makedirs(log_path, exist_ok=True)
log_filename = f'{log_path}/{LOG_NAME}.{datetime.datetime.today().date()}.log'
handler = logging.handlers.RotatingFileHandler(log_filename, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8')

# 设置默认handler
fmt = '%(asctime)s -[%(filename)s-%(lineno)d行(%(funcName)s)]进程%(process)d -%(levelname)s- %(message)s'
date_fmt = '%Y-%m-%d %H:%M:%S'
handler.setFormatter(logging.Formatter(fmt, date_fmt))
handler.setLevel(logging.DEBUG)

# 设置默认logger
logger = logging.getLogger(LOG_NAME)
logger.addHandler(handler)
logger.setLevel(logging.INFO)  #覆盖默认handler的Level
