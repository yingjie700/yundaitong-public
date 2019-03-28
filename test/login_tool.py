# coding=gbk
import re
import paramiko
from selenium import webdriver
import time

web = webdriver.Chrome()
url = 'http://10.1.1.116:8311/risk/business/amMyCustomer'
#url = 'https://ph-test.yscredit.com/risk/business/amFenceMarketing'
web.implicitly_wait(4)
web.get(url)
web.maximize_window()
web.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/a[2]').click()
time.sleep(2)
web.find_element_by_xpath('//*[@id="toggleCenter"]').click()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("10.1.1.116", port=22, username="yscredit", password="yscredit116")

ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
    "tail -n 1000 /home/yscredit/tomcat/logs/ccb-riskEntry.log | grep 'VerifyCodeController'")
tupian = (ssh_stdout.read().decode('utf-8'))
pattern = re.compile(r'(?<=生成图片验证码：)\d+\.?\d*')
result1 = pattern.findall(tupian)
tupianyanzhengma = str(result1[len(result1) - 1])
print(tupianyanzhengma)
web.find_element_by_xpath('//*[@id="callPhone"]').send_keys('18000000020')
web.find_element_by_xpath('//*[@id="returnCode"]').send_keys(tupianyanzhengma)
web.find_element_by_xpath('//*[@id="AutoCode"]').click()
time.sleep(1)
stdin, stdout, stderr = ssh.exec_command(
    "tail -n 100 /home/yscredit/tomcat/logs/ccb-riskEntry.log | grep 'SMSController'")
shouji = (stdout.read().decode('utf-8'))
result = re.findall(".*验证码：(.*)，请在.*", shouji)
shoujiyanzhengma = str(result[len(result) - 1])
print(shoujiyanzhengma)
# print(result)
ssh.close()
web.find_element_by_xpath('//*[@id="AutoCode2"]').send_keys(shoujiyanzhengma)
web.find_element_by_xpath('//*[@id="applyFor3"]').click()  # 登陆按钮1、2、3
