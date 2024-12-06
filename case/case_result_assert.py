import jsonpath
import pytest
import json
import sys
import os

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))))
from common import connect_data
from log import record_log

logger = record_log.record_log()


def case_result_assert(r, case_code=None, case_result=None):
    """
    封装断言方法
    若result开头为$,则用json提取式提取接口返回数据断言
    若result开头为select，则查数据库断言
    其余方式直接判等
    :param r: 接口返回结果
    :param case_code: 用例状态码
    :param case_result: 测试用例期望
    :return:
    """
    if case_result or case_code:
        if case_result:
            case_result = case_result.split(';')
            logger.debug('判断状态码')
            assert r['code'] == case_code
            for m in case_result:
                m = eval(m)
                expect = m['expect']
                result = m['result']
                if expect[0:6] == 'select':
                    sql_data = connect_data.connect_data(expect)
                    result = jsonpath.jsonpath(r, result)[0]
                    logger.debug(f'期望值查询数据库，查询结果为【{sql_data}】')
                    logger.debug(f'使用json提取式，提取结果为【{result}】')
                    assert sql_data[0][0] == result
                else:
                    result = jsonpath.jsonpath(r, result)[0]
                    logger.debug(f'期望值为固定值【{expect}】')
                    logger.debug(f'使用json提取式，提取结果为【{result}】')
                    assert result == expect
        else:
            logger.debug('只判断状态码')
            assert r['code'] == case_code
    else:
        logger.info('无期望结果和状态码')

# """
# 封装断言方法
# """
# # 获取用例中期望的状态code
# case_code = int(data[readcasedata.excelvalue().case_code])
#
# # def case_result_assert(r):
# #     # 判断期望是否根据数据库查询得到
# #     if data[readcasedata.excelvalue().case_isConnectSQL] == '是':
# #         logger.debug('使用数据库断言')
# #         # 将用例中的sql语句传到封装的数据库方法中
# #         sql_data = connect_data.connect_data(data[readcasedata.excelvalue().case_result])
# #         # 判断状态码
# #         assert r.json()['code'] == case_code
# #         # 判断响应数据
# #         assert sql_data[0][0] in json.dumps(r.json(), ensure_ascii=False)
# #     else:
# #         logger.debug('使用期望断言')
# #         # 判断状态码
# #         assert r.json()['code'] == case_code
# #         # 判断响应数据
# #         assert data[readcasedata.excelvalue().case_result] in json.dumps(r.json(), ensure_ascii=False)
