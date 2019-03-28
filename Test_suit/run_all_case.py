import unittest
import time,os,sys,logging
from HTMLTestRunner import HTMLTestRunner

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + r'D:\yundaitong\log')  # 返回脚本的路径
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='log_test.log',
                    filemode='w')
logger = logging.getLogger()
# 待执行用例的目录
def allcase():
    case_dir = r"D:\yundaitong\Test_suit"
    #case_path=os.path.join(os.getcwd(),"case")
    testcase = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(case_dir,
                                                   pattern='test_get_wlhk_adress_api.py',
                                                   top_level_dir=None)
    # discover方法筛选出来的用例，循环添加到测试套件中
    # print(discover)
    for test_suite in discover:
        for test_case in test_suite:
            # 添加用例到testcase
            print(test_case)
            testcase.addTest(test_case)
    return testcase


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    filename='result.html'
    fp=open(filename,'wb')
    runner = HTMLTestRunner(stream=fp, title='测试报告', description='测试报告：')
    runner.run(allcase())
    fp.close()
