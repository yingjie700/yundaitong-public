import re
import paramiko
from selenium import webdriver
from config import config1
import unittest
import time
class Login_in_phone(unittest.TestCase):
    def setUp(self):
        self.web = webdriver.Chrome()

    def tearDown(self):
        self.web.quit()

    def login_in_phone(self,phonenum,user='toggleRight',applyid='3'):  #toggleLeft、toggleCenter、toggleRight
        url='http://10.1.1.1:8311/loginIndex'
        #url='https://ph-test.yscredit.com'

        self.web.implicitly_wait(4)
        self.web.get(url)
        self.web.maximize_window()
        self.web.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/a[2]').click()
        time.sleep(2)
        self.web.find_element_by_xpath('//*[@id="%s"]'%user).click()
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("10.1.1.1", port=22, username="yscredit", password="ys12358d")

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("tail -n 1000 /home/yscredit/tomcat/logs/ccb-riskEntry.log | grep 'VerifyCodeController'")
        tupian=(ssh_stdout.read().decode('utf-8'))
        pattern = re.compile(r'(?<=生成图片验证码：)\d+\.?\d*')
        result1=pattern.findall(tupian)
        tupianyanzhengma=str(result1[len(result1)-1])
        print(tupianyanzhengma)

        self.web.find_element_by_xpath('//*[@id="callPhone"]').send_keys(phonenum)
        self.web.find_element_by_xpath('//*[@id="returnCode"]').send_keys(tupianyanzhengma)
        self.web.find_element_by_xpath('//*[@id="AutoCode"]').click()
        stdin, stdout, stderr = ssh.exec_command("tail -n 1000 /home/yscredit/tomcat/logs/ccb-riskEntry.log | grep 'SMSController'")
        shouji=(stdout.read().decode('utf-8'))
        result=re.findall(".*验证码：(.*)，请在.*",shouji)
        shoujiyanzhengma=str(result[len(result)-1])
        print(shoujiyanzhengma)
        print(result)
        ssh.close()
        self.web.find_element_by_xpath('//*[@id="AutoCode2"]').send_keys(shoujiyanzhengma)
        self.web.find_element_by_xpath('//*[@id="applyFor%s"]'% applyid).click() #登陆按钮1、2、3

    def test_tangxi_11(self,phonenum='18000000011'):
        self.login_in_phone(phonenum)#塘西支行
        self.web.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[3]/a/i').click()
        try:
            adress_find=self.web.find_elements_by_xpath('//*[@id="baseTable0"]/li/div[2]/div[1]/span[5]')
            adress_list=[]
            for adress in adress_find:
                adress_list.append(adress.text)
            print(adress_list)
            try:
                page_path=self.web.find_elements_by_xpath('//*[@id="outer0"]/div/span')
                print('find page path')
                if len(page_path)>3:
                    print(len(page_path))
                    total_page=len(page_path)-2

                    for page in range(1,total_page):
                        self.web.find_element_by_xpath('//*[@id="outer0"]/div/span['+str(page+3)+']').click()
                        time.sleep(2)
                        print(self.web.find_element_by_xpath('//*[@id="outer0"]/div/span['+str(page+3)+']').text)
                        adress_find=self.web.find_element_by_xpath('//*[@id="baseTable0"]/li/div[2]/div[1]/span[5]')
                        print(adress_find.text)
                        for second_adress in adress_find:
                            adress_list.append(second_adress.text)
                        print(adress_list)
                else:
                    self.web.find_element_by_xpath('//*[@id="detailTitle1"]').click()
            except:
                self.web.find_element_by_xpath('//*[@id="detailTitle1"]').click()

        except:
            self.web.find_element_by_xpath('//*[@id="detailTitle1"]').click()

        try:
            adress_find=self.web.find_elements_by_xpath('//*[@id="baseTable1"]/li/div[2]/div[1]/span[5]')
            adress_list2=[]
            for adress in adress_find:
                adress_list2.append(adress.text)
            print(adress_list2)
            try:
                page_path=self.web.find_elements_by_xpath('//*[@id="outer1"]/div')
                if len(page_path)>3:
                    total_page=len(page_path)-2
                    for page in range(1,total_page):
                        self.web.find_element_by_xpath('//*[@id="outer1"]/div/span['+str(page+3)+']').click()
                        time.sleep(2)
                        print(self.web.find_element_by_xpath('//*[@id="outer1"]/div/span['+str(page+3)+']').text)
                        adress_find=self.web.find_elements_by_xpath('//*[@id="baseTable1"]/li/div[2]/div[1]/span[5]')
                        print(adress_find.text)
                        for second_adress in adress_find:
                            adress_list2.append(second_adress.text)
                        print(adress_list2)
                else:
                    self.web.find_element_by_xpath('//*[@id="detailTitle2"]').click()
            except:
                self.web.find_element_by_xpath('//*[@id="detailTitle2"]').click()

        except:
            self.web.find_element_by_xpath('//*[@id="detailTitle2"]').click()

        try:
            adress_find=self.web.find_elements_by_xpath('//*[@id="baseTable2"]/li/div[2]/div[1]/span[5]')
            adress_list3=[]
            for adress in adress_find:
                adress_list3.append(adress.text)
            print(adress_list3)
            try:
                page_path=self.web.find_elements_by_xpath('//*[@id="outer2"]/div')
                if len(page_path)>3:
                    total_page=len(page_path)-2
                    for page in range(1,total_page):
                        self.web.find_element_by_xpath('//*[@id="outer2"]/div/span['+str(page+3)+']').click()
                        time.sleep(2)
                        print(self.web.find_element_by_xpath('//*[@id="outer2"]/div/span['+str(page+3)+']').text)

                        adress_find=self.web.find_elements_by_xpath('//*[@id="baseTable2"]/li/div[2]/div[1]/span[5]')
                        print(adress_find.text)
                        for second_adress in adress_find:
                            adress_list3.append(second_adress.text)
                        print(adress_list3)
                else:
                    print('1')
            except:
                print('2')
        except:
            print('3')
    def test_liangzhu_12(self):
        self.test_tangxi_11('18000000012')
    def test_lingping_13(self):
        self.test_tangxi_11('18000000013')
    def test_pingyao_15(self):
        self.test_tangxi_11('18000000015')
    def test_qiaosi_16(self):
        self.test_tangxi_11('18000000016')
    def test_dongfang_17(self):
        self.test_tangxi_11('18000000017')
    def test_xingqiao_18(self):
        self.test_tangxi_11('18000000018')
    def test_liancheng_19(self):
        self.test_tangxi_11('18000000019')
    def test_xixi_20(self):
        self.test_tangxi_11('18000000020')
    def test_xianling_21(self):
        self.test_tangxi_11('18000000021')
    def test_gouzhuang_22(self):
        self.test_tangxi_11('18000000022')
    def test_taiyan_23(self):
        self.test_tangxi_11('18000000023')
    def test_yuhang_24(self):
        self.test_tangxi_11('18000000024')
    def test_chengbei_25(self):
        self.test_tangxi_11('18000000025')
    def test_chongxian_26(self):
        self.test_tangxi_11('18000000026')
    def test_chengxi_27(self):
        self.test_tangxi_11('18000000027')
    def test_linpingxingcheng_28(self):
        self.test_tangxi_11('18000000028')
if __name__ == "__main__":
    unittest.main()
