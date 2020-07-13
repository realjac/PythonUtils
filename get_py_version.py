"""获取python执行版本，用于兼容"""
import sys

PY2 = False
PY3 = False


def python_version():
    version = sys.version[0]
    # sys.version 返回版本信息字符串 3.7.0......
    if version == '2':
        global PY2
        PY2 = True
    else:
        global PY3
        PY3 = True
    return


# 导包时直接执行获取到版本信息
python_version()
