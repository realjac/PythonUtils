import getopt
import os
import re
import sys


def parse_args():
    """
        命令行参数解析
    """

    path = ''

    try:

        opts, args = getopt.getopt(sys.argv[1:], "hp:", ["help", "path="])
    except getopt.GetoptError:
        print(f"Usage: python3 {sys.argv[0]}  -p <api path>")
        print(f"Or: python3 {sys.argv[0]}  --path=<api path>")
        print(f"For help: python3 {sys.argv[0]}  --help/-h ")
        sys.exit(2)
        
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("功能：提取git中controller下的api的uri")
            print("请输入controller文件夹的路径")
            print(f"Usage: python3 {sys.argv[0]}  <api path>")
            print(f"Usage: python3 {sys.argv[0]}  -p <api path>")
            print(f"Or: python3 {sys.argv[0]}  --path=<api path>")
            sys.exit(2)
        elif opt in ("-p", "--path"):
            path = arg

    # 不含'-'或'--'的参数。
    for i in range(0, len(args)):
        if os.path.isdir(args[i]):
            path = args[i]

    return path


def find_file_content(file_path: str) -> list:
    """查找文件内容，获取api接口"""

    # 文件路径转换为api路径
    try:
        api_path = re.match(r'^.*controller[s]?(/[\w|/]+)_controller.*', file_path).group(1)
    except:
        raise AssertionError(f'不是controller文件:{file_path}')

    with open(file_path) as f:
        lines = f.readlines()

    result = []
    for l in range(len(lines)):
        m = re.match(r'.*public function.*', lines[l])
        if m:
            func_name = re.match(r'^public function (\w*)\(', m.group().strip()).group(1).strip()
            if not func_name.startswith('_'):
                # 向上回溯5行，取函数功能名称
                usage_name = ''
                for i in range(6):
                    # 取有汉字的行
                    usage = re.match(r'^.*([\u4e00-\u9fff]+)\w*', lines[l - i - 1])
                    if usage:
                        # 只取汉字、英文、数字字符
                        usage_name = ''.join([_ for _ in usage.group() if
                                              '\u4e00' <= _ <= '\u9fff' or u'\u0030' <= _ <= u'\u007A']) + usage_name
                    # 如果遇到{}，则认为遇到了上一个函数，结束向上回溯
                    if re.match(r'.*[{|}]+.*', lines[l - i - 1]):
                        break

                result.append(api_path + '/' + func_name + ',' + usage_name)
    return result


def main(path: str):
    # 遍历目录下所有文件
    file_list = []
    g = os.walk(path, topdown=False)
    for root, dir_names, file_names in g:
        for f in file_names:
            file_list.append(os.path.join(root, f))
    # 可以过滤一些文件
    ignore_pattern = [
        # 'cron*',
        'xxxxxxxxx'
    ]
    ignore_regex = re.compile(r'(' + '|'.join(ignore_pattern) + ')', re.I)
    file_list = list(filter(lambda x:not ignore_regex.search(x), file_list))
    # print(file_list)
    for file in file_list:
        try:
            # result = find_file_content(file)
            for i in find_file_content(file):
                print(i)
        except Exception as  e:
            print(e)
            pass


if __name__ == '__main__':
    # 参数：api文件所在目录
    main(parse_args())
