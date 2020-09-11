#!/usr/bin/python3
# _*_ coding:UTF-8 _*_
# @filename: config/config.py

REDIS_CONFIG = {
    "host"            :"127.0.0.1",
    "port"            :6379,
    "db"              :0,
    "password"        :"",
    "max_connections" :40,
    "socket_timeout"  :1,
    "decode_responses":True
}


#导入某些线上配置，包括线上redis等
try:
    from config.secrets import *
except Exception as e:
    print('配置文件导入失败，{}'.format(e))
