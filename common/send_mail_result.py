import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import os
import sys
import json

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))))
from common.readConfig import readConfig


def send_mail_result(run_result, e=None):
    """
    邮件发送测试报告及报告压缩文件
    :param run_result: 测试执行结果
    :param e: 执行过程中抛出的异常
    :return:
    """
    rd = readConfig('mail.ini')

    # 定义通过数、失败次数
    pass_count = 0
    fail_count = 0
    result_json = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\report\\html\\data\\behaviors.json')))
    json_file = open(result_json, 'r', encoding="utf-8")
    json_data = json.load(json_file)
    b = json_data['children']
    for i in b:
        if i['status'] == 'passed':
            pass_count += 1
        elif i['status'] == 'failed':
            fail_count += 1
    # 执行用例数
    case_datas = pass_count + fail_count

    mail_host = rd.read_mail_conf('mail_host')  # 设置服务器
    mail_user = rd.read_mail_conf('mail_user')  # 用户名
    mail_pass = rd.read_mail_conf('mail_pass')  # 口令
    project_name = rd.read_mail_conf('project_name')  # 项目名称

    sender = mail_user
    receivers = rd.read_mail_conf('receivers').split(';')

    # 编辑邮件内容
    message = MIMEMultipart()
    message['From'] = Header(mail_user, 'us-ascii')
    message['To'] = Header('all', 'us-ascii')
    subject = f'{project_name}接口自动化测试报告'
    message['Subject'] = Header(subject, 'utf-8')

    if run_result == 'success':
        mail_text = f'''各位同事/领导好：\n
        以下内容为本次【{project_name}】项目接口测试大致报告:\n
        本次执行测试用例{case_datas}条\n
        其中通过{pass_count}条；失败{fail_count}条；通过率为{(pass_count / case_datas * 100)}%\n
        详细测试报告内容参考附件！
        '''

        # 邮件正文内容
        message.attach(MIMEText(mail_text, 'plain', 'utf-8'))

        # 构造附件1，传送日志文件
        log_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\log\\record_log.log')))
        att1 = MIMEText(open(log_path, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1["Content-Disposition"] = 'attachment; filename="record_log.log"'
        message.attach(att1)

        # 构造附件2，传送报告压缩文件
        result_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\report\\test_result.zip')))
        att2 = MIMEText(open(result_path, 'rb').read(), 'base64', 'utf-8')
        att2["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att2["Content-Disposition"] = 'attachment; filename="test_result.zip"'
        message.attach(att2)
    else:
        mail_text = f'''各位同事/领导好：\n
        本次【{project_name}】项目接口测试失败，具体原因如下：\n
        {e}'''

        # 邮件正文内容
        message.attach(MIMEText(mail_text, 'plain', 'utf-8'))

        # 构造附件1，传送日志文件
        log_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\log\\record_log.log')))
        att1 = MIMEText(open(log_path, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1["Content-Disposition"] = 'attachment; filename="record_log.log"'
        message.attach(att1)


    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件" + str(e))
    finally:
        json_file.close()
        smtpObj.close()
#
#
# if __name__ == '__main__':
#     send_mail_result()
