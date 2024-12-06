import requests
import sys
import os

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../common'))))
from readConfig import readConfig

def get_cookie():
    """
    获取cookie
    :return:
    """
    # 调用读取文件类
    rc = readConfig('conf.ini')
    # 读取环境登录url
    login_url = rc.read_test_evn('login_url')
    # 读取登录账户信息
    userid = rc.read_test_usr('usr')
    pwd = rc.read_test_usr('pwd')
    # 根据测试环境参数修改登录接口传参
    r = requests.post(login_url, data={"username": userid, "password": pwd}, verify=False, allow_redirects=False)
    cookies = r.cookies.get_dict()
    print(r)
    # 将获取的cookie重新拼装
    cookies = "SESSION=" + cookies['SESSION']
    return cookies