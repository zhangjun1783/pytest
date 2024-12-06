import os
import re
import sys


# 获取用例文件路径
def case_filepath(case_name):
    filepath = os.path.join(os.path.dirname(__file__), '..\\data')
    if os.path.isdir(filepath):
        filelist = os.listdir(filepath)
        for f in filelist:
            res = re.match(case_name, f, re.I)
            if res:
                f = res.group()
                f = os.path.join(filepath, f)
                return f
