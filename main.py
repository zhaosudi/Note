import unittest
import os
from BeautifulReport import BeautifulReport

DIR = os.path.dirname(os.path.abspath(__file__))
Environ = "/env_config/online"


def run(test_suite):
    # 定义输出的文件位置和名字
    filename = "report.html"
    result = BeautifulReport(test_suite)
    result.report(filename=filename, description='测试报告', report_dir=DIR)


if __name__ == '__main__':
    testsuite = unittest.defaultTestLoader.discover(
        start_dir=DIR + '/TestCase',
        pattern="test*.py"
    )
    run(testsuite)
