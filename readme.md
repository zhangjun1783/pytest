[TOC]

# Pytest+requests+allure+excel+log+mail+配置文件接口自动化测试框架
## 一、目录结构
```
│  readme.md
│  requirements.txt
│  run.py            
├─case
│  │  test_case_encapsulation.py # 测试方法
│  │  case_result_assert.py # 封装断言方法
│          
├─common # 公共方法
│  │  connect_data.py # 数据库连接封装
│  │  get_cookie.py # 获取环境cookie封装
│  │  case_filepath.py # 获取测试用例路径
│  │  readcasedata.py # 读取测试用例数据封装
│  │  readConfig.py # 读取配置封装
│  │  send_mail_result.py # 邮件发送封装
│  │  zip_result.py # 压缩文件封装
│          
├─config # 配置环境
│      conf.ini # 环境配置
│      log.ini # 日志配置
│      mail.ini # 邮件配置
│      
├─data # 测试用例
│      data.xls # 测试用例
│      
├─log # 日志文件
│  │  record_log.py # 日志方法封装
│          
└─report # 测试报告
```
## 二、环境配置
+ 使用时，在终端使用```pip install -r requirements.txt```
```
allure-pytest==2.9.45
allure-python-commons==2.9.45
async-generator==1.10
atomicwrites==1.4.0
attrs==21.4.0
beautifulsoup4==4.11.1
certifi==2021.10.8
cffi==1.15.0
charset-normalizer==2.0.12
click==8.1.3
colorama==0.4.4
cryptography==37.0.2
cssselect==1.1.0
demjson==2.2.4
Flask==2.1.2
freegames==2.4.0
h11==0.13.0
idna==3.3
importlib-metadata==4.11.3
iniconfig==1.1.1
itsdangerous==2.1.2
Jinja2==3.1.2
jsonpath==0.82
lxml==4.8.0
MarkupSafe==2.1.1
mysqlclient==2.1.0
outcome==1.1.0
packaging==21.3
pluggy==1.0.0
py==1.11.0
pycparser==2.21
PyMySQL==1.0.2
pyOpenSSL==22.0.0
pyparsing==3.0.8
pyquery==1.4.3
PySocks==1.7.1
pytest==7.1.2
pytest-assume==2.4.3
pytest-html==3.1.1
pytest-metadata==2.0.1
requests==2.27.1
selenium==4.1.5
six==1.16.0
sniffio==1.2.0
sortedcontainers==2.4.0
soupsieve==2.3.2.post1
tomli==2.0.1
trio==0.20.0
trio-websocket==0.9.2
typing_extensions==4.2.0
urllib3==1.26.9
Werkzeug==2.1.2
wsproto==1.1.0
xlrd==2.0.1
XlsxWriter==3.0.3
xlutils==2.0.0
xlwt==1.3.0
zipp==3.8.0
```
## 三、使用介绍
### 3.1 配置环境
+ 在config文件夹下配置conf.ini
```ini
#测试环境登录接口
[TEST_EVN]
# 格式参照：http://xxxx:xx/xxx
# 登录接口的url,主要作用为前置条件需要登录的接口获取cookie
login_url = http://xxxx:xx/xxx

#测试账户
[TEST_USER]
usr = xxx
pwd = xxx

# 数据库配置信息
[TEST_DATA]
host = xxx
port = xxx
user = xxx
password = xxx
database = xxx
charset = utf8
```
+ 配置mail.ini(若测试不需要发送邮件即可忽略)
```ini
[MAIL]
# 设置服务器
mail_host=xxx
# 用户名
mail_user=xxx
# 口令
mail_pass=xxx
# 接收邮件的邮箱，若接收为多个时，以;隔开
receivers=xxx
# 项目名称
project_name=xxx
```
+ 在run.py中配置报告输出方式，主函数run('mail')
  + 同时也可将mail修改为htnl
  + mail是通过邮件输出测试报告
  + html则是弹窗输出测试报告
```python
import allure
import pytest
import traceback
from common import send_mail_result
from common import zip_result
from log.record_log import run_log as logger


def run(result_type):
    """执行并生成allure测试报告"""
    try:
        # 运行输出并在report/result目录下生成json文件
        pytest.main(["-s", "-v", "--alluredir", "report/result"])
        # 通过标准库中的subprocess包来fork一个子进程，并进行一个外部的程序
        import subprocess
        # 读取json文件并生成html报告，--clean若目录存在则Y先清除
        subprocess.call('allure generate report/result/ -o report/html --clean', shell=True)
        # 判断报告输出方式
        if result_type == 'mail':
            run_result = 'success'
            # 压缩生成的测试报告文件
            zip_result.zip_result()
            # 发送邮件
            send_mail_result.send_mail_result(run_result)
        elif result_type == 'html':
            # 生成一个本地的服务并自动打开html报告
            subprocess.call('allure open -h 127.0.0.1 -p 9999 report/html', shell=True)
        # 若输出方式不在范围内，直接抛出异常（同时也可在代码中扩展新的方式）    
        else:
            raise '暂不支持该方式输出'
    except Exception:
        e = traceback.format_exc()
        run_result = 'fail'
        logger.error('生成报告失败，具体原因：'+str(e))
        send_mail_result.send_mail_result(run_result, e)


if __name__ == '__main__':
    run('html')
```
### 3.2 测试用例维护
+ 在data文件下，测试用例直接维护在data.xls文件上,详细参照该文档即可
+ 在common下的readcasedata.py用于读取excel中测试用例数据，若测试模板有更新，维护该模板即可
```python
import xlrd
import sys

sys.path.append("..")
from common import case_filepath


class ReadCaseData:
    """
    封装读取测试数据
    """

    def get_sheet(self, sheet_name):
        """
        获取excel的sheet页
        :return: 返回sheet页
        """
        book = xlrd.open_workbook(case_filepath.case_filepath('case_data.xls'))
        return book.sheet_by_name(sheet_name)

    def get_exceldatas(self):
        """
        获取测试用例sheet页数据
        :return: 返回测试用例数据
        """
        # 定义空列表,获取执行的模块名
        execute_sheets = []
        # 定义空列表,返回用例数据
        data = []
        for m in range(1, self.get_sheet('首页').nrows):
            if self.get_sheet('首页').cell_value(m, 1) == 'Y':
                execute_sheets.append(self.get_sheet('首页').cell_value(m, 0))
        for execute_sheet in execute_sheets:
            execute = self.get_sheet(execute_sheet)
            # 获取表格第一行作为标题
            title = execute.row_values(0)
            for i in range(1, execute.nrows):
                row_value = execute.row_values(i)
                data.append(dict(zip(title, row_value)))
        return data

    def user_params(self):
        """
        获取用户参数
        :return: 以字典返回用户参数
        """
        params_sheet = self.get_sheet('用户参数')
        # 定义参数空字典
        params_values = {}
        for i in range(1, params_sheet.nrows):
            params_values[params_sheet.cell_value(i, 0)] = params_sheet.cell_value(i, 1)
        return params_values


class excelvalue():
    # case_Id = "用例Id"
    case_module = "用例模块"
    case_name = "用例名称"
    case_ip_port = "测试环境"
    case_url = "用例地址"
    case_method = "请求方式"
    case_type = "请求类型"
    case_data = "请求参数"
    case_headers = "请求头"
    # case_preposition = "前置条件"
    case_processing = "后置处理"
    case_code = "状态码"
    case_result = "期望"
```
### 3.4 测试方法介绍
+ 在case文件下，根据注释理解即可
```python
import os
import sys
import jsonpath
import pytest
import requests
import json
import case_result_assert
from demjson import decode

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
```
### 3.5 断言方法封装
+ 在case目录下的case_result_assert.py文件中
  ```python
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
                  if result[0] == '$':
                      result = jsonpath.jsonpath(r, result)[0]
                      logger.debug(f'使用json提取式，提取结果为【{result}】')
                      assert expect == result
                  elif result[0:6] == 'select':
                      sql_data = connect_data.connect_data(result)
                      logger.debug(f'使用数据库断言，查询结果为【{sql_data}】')
                      assert sql_data[0][0] == expect
                  else:
                      logger.debug('直接判断期望与结果')
                      assert expect == result
          else:
              logger.debug('只判断状态码')
              assert r['code'] == case_code
      else:
          logger.info('无期望结果和状态码')
  ```
### 3.6 日志介绍

+ 使用日志配置文件和logging.config实现
  + 日志配置文件
  ```ini
  [loggers]
  keys=root
  
  [handlers]
  keys=consoleHandler,fileHandler
  
  [formatters]
  keys=simpleFormatter
  
  [logger_root]
  level=DEBUG
  handlers=consoleHandler,fileHandler
  
  [handler_consoleHandler] #输出到控制台的handler
  class=StreamHandler
  level=DEBUG
  formatter=simpleFormatter
  args=(sys.stdout,)
  
  [handler_fileHandler] #输出到日志文件的handler
  class=logging.handlers.TimedRotatingFileHandler
  level=INFO
  formatter=simpleFormatter
  args=('log/record_log.log','midnight',1,7,'utf-8')
  
  [formatter_simpleFormatter] #定义日志文件的格式
  format=[%(asctime)s-%(name)s(%(levelname)s)%(filename)s:%(lineno)d]%(message)s
  datefmt=%Y-%m-%d %H:%M:%S
  ```
  + 日志封装，需要使用时，直接引用该方法下的run_log（参考测试方法介绍中的引用方式）
  ```python
  import logging
  import logging.handlers
  import logging.config
  import os
  import sys
  
  """
  读取日志配置文件，并实例化run_log
  """
  
  
  def record_log():
      filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config/log.ini'))
      logging.config.fileConfig(filename)
      return logging.getLogger()
  
  
  def close_log():
      return logging.shutdown()
  ```

### 3.7 调用

运行主程序即可