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
            if self.get_sheet('首页').cell_value(m, 1) == 'Y' or self.get_sheet('首页').cell_value(m, 1) == 'y':
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

#
# if __name__ == '__main__':
#     h = ReadCaseData().get_exceldatas()
#     for m in h:
#         print(h[m])