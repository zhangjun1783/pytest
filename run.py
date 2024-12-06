import allure
import pytest
import traceback
import time
import os
import sys
from common import send_mail_result
from common import zip_result
from log import record_log
from common import readConfig


def run(result_type):
    """执行并生成allure测试报告"""
    # 判断report文件夹下是否存在报告文件,若存在清除上一次报告内容
    report_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), 'report\\allure-results')))
    if os.path.exists(report_path):
        # windows cmd命令
        cmd = f'rd /S /Q {report_path}'
        # os运行
        os.system(cmd)
        print(cmd)
    else:
        pass

    # 判断log文件夹下是否存在日志文件，若存在则备份
    record_log_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), 'log\\record_log.log')))
    if os.path.exists(record_log_path):
        rename_log_path = (
            os.path.abspath(os.path.join(os.path.dirname(__file__), f'log\\record_log_{time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime())}.log.')))
        os.renames(record_log_path, rename_log_path)
        print(record_log_path)
        print(rename_log_path)
    else:
        pass

    # 日志调用实例化
    logger = record_log.record_log()
    # 获取项目名称
    mail_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), 'config\\mail.ini')))
    rc = readConfig.readConfig(mail_path)
    project_name = rc.read_mail_conf('project_name')
    # 日志打印项目开始
    logger.info(f"""
                                 _    _         _      _____         _
                  __ _ _ __ (_)  / \\  _   _| |_ __|_   _|__  ___| |_
                 / _` | '_ \\| | / _ \\| | | | __/ _ \\| |/ _ \\/ __| __|
                | (_| | |_) | |/ ___ \\ |_| | || (_) | |  __/\\__ \\ |_
                 \\__,_| .__/|_/_/   \\_\\__,_|\\__\\___/|_|\\___||___/\\__|
                      |_|
                      【{project_name}】项目测试开始，开始时间为{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}""")
    try:
        # 运行输出并在report/result目录下生成json文件
        pytest.main(["-s", "-v", "--alluredir", "report/allure-results"])
        # 通过标准库中的subprocess包来fork一个子进程，并进行一个外部的程序
        import subprocess
        # 读取json文件并生成html报告，--clean若目录存在则Y先清除
        subprocess.call('allure generate report/allure-results -o report/html --clean', shell=True)
        # 判断报告输出方式
        if result_type == 'mail':
            run_result = 'success'
            # 压缩生成的测试报告文件
            zip_result.zip_result()
            # 发送邮件
            send_mail_result.send_mail_result(run_result)
        elif result_type == 'html':
            # 生成一个本地的服务并自动打开html报告
            # print(1)
            subprocess.call('allure open -h 127.0.0.1 -p 9999 report/html', shell=True)
        # 若输出方式不在范围内，直接抛出异常（同时也可在代码中扩展新的方式）
        else:
            raise '暂不支持该方式输出'
    except Exception:
        e = traceback.format_exc()
        run_result = 'fail'
        logger.error('生成报告失败，具体原因：' + str(e))
        send_mail_result.send_mail_result(run_result, e)
    logger.info(f"""【{project_name}】项目测试结束，结束时间为{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}""")


if __name__ == '__main__':
    run('html')
    record_log.close_log()
