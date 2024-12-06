import pymysql
import sys
import os

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../common'))))
from readConfig import readConfig

def connect_data(sql):
    """
    连接数据库，并执行期望sql
    :param sql: 期望sql
    :return:
    """
    rc = readConfig('conf.ini')
    read_port = int(rc.read_data_conf('port'))
    connect = pymysql.connect(
        host=rc.read_data_conf('host'),
        port=read_port,
        user=rc.read_data_conf('user'),
        password=rc.read_data_conf('password'),
        database=rc.read_data_conf('database'),
        charset=rc.read_data_conf('charset')
    )
    cursor = connect.cursor()
    cursor.execute(sql)
    sql_data = cursor.fetchall()
    return sql_data

# if __name__ == '__main__':
#     sql_data = connect_data('select LABEL from t_basic_dict where ID=1')
#     print(sql_data)
