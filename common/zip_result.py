import zipfile
import os
import sys


def zip_result():
    """
    用于压缩测试报告的html文件
    :return:
    """
    sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))))
    dirpath = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../report/html')))
    outpath = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../report/test_result.zip')))
    zip = zipfile.ZipFile(outpath, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉⽬标跟路径，只对⽬标⽂件夹下边的⽂件及⽂件夹进⾏压缩
        fpath = path.replace(dirpath, '')
        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
            # print('aaaa')
    zip.close()

# if __name__ == '__main__':
#     zip_result()
