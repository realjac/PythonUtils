#!/usr/bin/python3

import getopt
import os
import sys

"""建议直接使用argparse模块，节省时间！https://docs.python.org/zh-cn/3/library/argparse.html
argparse 模块可以让人轻松编写用户友好的命令行接口。程序定义它需要的参数，
然后 argparse 将弄清如何从 sys.argv 解析出那些参数。 
argparse 模块还会自动生成帮助和使用手册，并在用户给程序传入无效参数时报出错误信息"""
# 1.参数：api文件所在目录

def parse_args():
    """
        命令行参数解析
        options, args = getopt.getopt(args, shortopts, longopts=[])

        参数args：一般是sys.argv[1:]。过滤掉sys.argv[0]，它是执行脚本的名字，不算做命令行参数。
        参数shortopts：短格式分析串。例如："hp:i:"，h后面没有冒号，表示后面不带参数；p和i后面带有冒号，表示后面带参数。
        参数longopts：长格式分析串列表。例如：["help", "ip=", "port="]，help后面没有等号，表示后面不带参数；ip和port后面带冒号，表示后面带参数。

        返回值options是以元组为元素的列表，每个元组的形式为：(选项串, 附加参数)，如：('-i', '192.168.0.1')
        返回值args是个列表，其中的元素是那些不含'-'或'--'的参数。
    """

    path = ''

    try:

        opts, args = getopt.getopt(sys.argv[1:], "hp:", ["help", "path="])
    except getopt.GetoptError:
        print(f"Usage: python3 {sys.argv[0]}  -p <api path>")
        print(f"Or: python3 {sys.argv[0]}  --path=<api path>")
        print(f"For help: python3 {sys.argv[0]}  --help/-h ")
        sys.exit(2)

    # 处理 返回值options是以元组为元素的列表。
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(f"Usage: python3 {sys.argv[0]}  <api path>")
            print(f"Usage: python3 {sys.argv[0]}  -p <api path>")
            print(f"Or: python3 {sys.argv[0]}  --path=<api path>")
            print(f"Example: python3 {sys.argv[0]} --path=~/pathA/projectA/web/api")
            sys.exit(2)
        elif opt in ("-p", "--path"):
            path = arg

    # 返回值args列表，即其中的元素是那些不含'-'或'--'的参数。
    for i in range(0, len(args)):
        if os.path.isdir(args[i]):
            path = args[i]

    return path


if __name__ == '__main__':
    parse_args()
