import os
import configparser


class readConfig():
    """
    此类用于读取配置文件的操作封装
    """

    def __init__(self, locator):
        self.locator = locator
        # 获取文件当前位置(此处避免出错，获取文件绝对位置)
        cur_path = os.path.dirname(os.path.abspath(__file__))
        # 拼接配置文件路径
        config_path = os.path.join(cur_path, "..\\config\\", self.locator)
        # 引用configparser类
        self.conf = configparser.ConfigParser()
        # 读取配置文件
        self.conf.read(config_path, encoding='utf-8')

    # 读取测试环境
    def read_test_evn(self, emo):
        test_evn = self.conf.get('TEST_EVN', emo)
        return test_evn

    # 读取测试账户
    def read_test_usr(self, msg):
        test_usr = self.conf.get('TEST_USER', msg)
        return test_usr

    # 读取数据库配置
    def read_data_conf(self, msg):
        data_conf = self.conf.get('TEST_DATA', msg)
        return data_conf

    # 读取邮箱信息
    def read_mail_conf(self, tp):
        mail_conf = self.conf.get('MAIL', tp)
        return mail_conf
