
import datetime
import logging
import logging.config
import os
import sys

# 兼容python2
if sys.version[0]=='2':
  reload(sys)
  sys.setdefaultencoding('utf-8')
  
# 通过日志文件的相对路径得到日志文件的绝对路径
LOG_HOME = '{}/../log'.format(os.path.split(os.path.realpath(__file__))[0])
os.makedirs(LOG_HOME, exist_ok=True)

def get_logger(name, conf=None, level='INFO'):
    if not name.endswith('.log'):
        log_file = '{}.log'.format(name)
    else:
        log_file = name
    path = os.path.join(LOG_HOME, log_file)
    if not conf:
        conf = {'version': 1,
                'disable_existing_loggers': False,
                'formatters': {
                    'default': {
                        'format': '%(asctime)s|%(levelname)s|%(name)s|%(module)s|%(filename)s|%(lineno)s|%(funcName)s)|%(message)s',
                        'datefmt':'%Y-%m-%d %H:%M:%S',
                    }
                },
                'handlers': {
                    name: {'()': logging.RotatingFileHandler,
                           'formatter': 'default',
                           'filename': path,
                           'maxBytes': 1024 * 1024 * 20,
                           'backupCount': 3}
                },
                'loggers': {
                    name: {
                        'handlers': [name],
                        'level': level,
                        'propagate': False,
                    }
                }}
    logging.config.dictConfig(conf)
    return logging.getLogger(name)


# 配置：
LOG_NAME = 'main'
logger = get_logger('{}.{}'.format(LOG_NAME,datetime.datetime.today().date()))
