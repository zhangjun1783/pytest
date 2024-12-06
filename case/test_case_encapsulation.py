import os
import sys
import jsonpath
import pytest
import requests
import json
import case_result_assert
#from demjson import decode

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))))
from common import get_cookie
from common import readcasedata
from log import record_log


"""
定义全局变量
"""
global_data = {}


def set_global_data(key, value):
    """
    设置全局变量，用于关联参数
    :return:
    """
    global_data[key] = value
    return global_data


def get_global_data(key):
    """
    从全局变量global_data中取值
    :return:
    """
    if key in global_data.keys():
        return global_data[key]
    else:
        return


"""
初始化数据
"""
# 初始化日志
logger = record_log.record_log()

# 获取cookie
cookies = get_cookie.get_cookie()

# 获取测试用例及数据
rcd = readcasedata.ReadCaseData()
data = rcd.get_exceldatas()
case_name = []
for m in data:
    case_name.append(f"{m['用例模块']}-{m['用例名称']}")
case_name = tuple(case_name)
logger.debug(cookies)

# 将用户变量存入全局变量
params_values = rcd.user_params()
logger.debug(f"用户参数为：{params_values}")
for params_values_key in params_values:
    set_global_data(params_values_key, params_values[params_values_key])



@pytest.mark.parametrize("data", data, ids=case_name)
def test_case(data):
    """
    @function:封装请求
    @param data:测试用例数据
    """
    # 获取请求头,给请求头添加cookie
    header = data[readcasedata.excelvalue().case_headers]
    if header:
        # 转换为字典
        header = json.loads(header)
    else:
        header = {}
    header['Cookie'] = cookies

    # 获取参数，对请求参数做处理
    params = data[readcasedata.excelvalue().case_data]
    params = eval(params)
    for param in params:
        if get_global_data(param):
            params[param] = get_global_data(param)
    params = json.dumps(params)

    # # 判断是否存在前置条件
    # case_prepositions = data[readcasedata.excelvalue().case_preposition]
    # if case_prepositions:
    #     case_prepositions = case_prepositions.split(';')
    #     for case_preposition in case_prepositions:
    #         # 判断是否需要登录，需要则添加cookie
    #         if case_preposition == 'login':
    #             header['Cookie'] = cookies
    #         # 获取全局变量
    #         else:
    #             case_preposition_value = get_global_data(case_preposition)[0]
    #             params = eval(params)
    #             params[case_preposition] = case_preposition_value
    #             params = json.dumps(params)

    # 对中文乱码做处理
    params = params.encode("utf-8").decode("unicode-escape")
    logger.info(f'用例标题：【{data[readcasedata.excelvalue().case_name]}】的参数为：{params}')
    # 执行用例
    if data[readcasedata.excelvalue().case_method] == 'get':
        r = requests.get(
            url=data[readcasedata.excelvalue().case_ip_port] + data[readcasedata.excelvalue().case_url],
            params=json.loads(params),
            headers=header
        )
    elif data[readcasedata.excelvalue().case_method] == 'post':
        if data[readcasedata.excelvalue().case_type] == 'json':
            r = requests.post(
                url=data[readcasedata.excelvalue().case_ip_port] + data[readcasedata.excelvalue().case_url],
                json=json.loads(params),
                headers=header)
        else:
            params = params.encode("utf-8").decode("latin-1")
            r = requests.post(
                url=data[readcasedata.excelvalue().case_ip_port] + data[readcasedata.excelvalue().case_url],
                data=json.loads(params),
                headers=header)
    else:
        logger.error('请求方法暂不支持')
    # 打印相关参数日志
    logger.debug(f"请求url【{r.url}】")
    logger.info(f'用例标题：【{data[readcasedata.excelvalue().case_name]}】的返回值为：{r.json()}')
    logger.debug(f'用例标题：【{data[readcasedata.excelvalue().case_name]}】的请求头为：{r.headers}')

    case_code = data[readcasedata.excelvalue().case_code]
    case_result = data[readcasedata.excelvalue().case_result]
    # 调取封装的断言方法
    try:
        h = r.json()
        case_result_assert.case_result_assert(h, case_code, case_result)
        logger.info('用例标题：【' + data[readcasedata.excelvalue().case_name] + '】测试通过')
    except AssertionError as a:
        logger.warning('用例标题：【' + data[readcasedata.excelvalue().case_name] + '】断言不通过，原因：' + str(a))
        raise

    # 后置处理，提取全局变量
    if data[readcasedata.excelvalue().case_processing]:
        case_processings = data[readcasedata.excelvalue().case_processing].split(';')
        for case_processing in case_processings:
            case_processing_header = case_processing.split('.')[-1]
            case_processing_value = jsonpath.jsonpath(r.json(), case_processing)
            set_global_data(case_processing_header, case_processing_value)
            logger.debug(get_global_data('patientname'))
#
#
# if __name__ == "__main__":
#     # """执行并生成allure测试报告"""
#     pytest.main(["-s", "-v", "--alluredir", "../report/result"])  # 运行输出并在report/result目录下生成json文件
#     import subprocess  # 通过标准库中的subprocess包来fork一个子进程，并进行一个外部的程序
#     # 读取json文件并生成html报告，--clean若目录存在则Y先清除
#     subprocess.call('allure generate ../report/result/ -o ../report/html --clean', shell=True)
#     # 生成一个本地的服务并自动打开html报告
#     subprocess.call('allure open -h 127.0.0.1 -p 9999 ../report/html', shell=True)
