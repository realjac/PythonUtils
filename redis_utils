#!/usr/bin/python3
# _*_ coding:UTF-8 _*_


import redis

from config import config


def get_config_redis():
    try:
        return redis.Redis(**config.REDIS_CONFIG)
    except Exception as e:
        raise e


def get_redis_client(ip, port=6379, password=None):
    try:
        redis_client = redis.Redis(host=ip, port=port, password=password)
    except Exception as e:
        raise e
    return redis_client


def get_redis_pool(ip, port=6379, password=None):
    """
     用于实现多个Redis实例共享一个连接池
    :param ip:
    :param port:
    :param password:
    :return: redis_client
    """
    pool = redis.ConnectionPool(ip, port)
    try:
        redis_client = redis.Redis(connection_pool=pool, password=password)
    except Exception as e:
        raise e
    return redis_client
