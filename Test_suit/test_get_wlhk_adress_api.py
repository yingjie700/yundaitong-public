# coding=gbk
from selenium.webdriver.common.action_chains import ActionChains
import re
import paramiko
import json
from selenium import webdriver
import unittest
import time
import requests

class Login_in_phone(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.web = webdriver.Chrome()
        url = 'http://10.1.1.1:8311/loginIndex'
        #url='https://ph-test.yscredit.com/risk/business/amFenceMarketing'
        self.web.implicitly_wait(4)
        self.web.get(url)
        self.web.maximize_window()
    @classmethod
    def tearDownClass(self):
        self.web.quit()
    def login_in_phone(self,phonenum,user='toggleCenter',applyid='3'):#toggleLeft��toggleCenter��toggleRight
        self.web.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/a[2]').click()
        time.sleep(2)
        self.web.find_element_by_xpath('//*[@id="%s"]'%user).click()
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("10.1.1.1", port=22, username="yscredit", password="ys12358d")

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("tail -n 1000 /home/yscredit/tomcat/logs/ccb-riskEntry.log | grep 'VerifyCodeController'")
        tupian=(ssh_stdout.read().decode('utf-8'))
        pattern = re.compile(r'(?<=����ͼƬ��֤�룺)\d+\.?\d*')
        result1=pattern.findall(tupian)
        tupianyanzhengma=str(result1[len(result1)-1])
        print(tupianyanzhengma)
        self.web.find_element_by_xpath('//*[@id="callPhone"]').send_keys(phonenum)
        self.web.find_element_by_xpath('//*[@id="returnCode"]').send_keys(tupianyanzhengma)
        self.web.find_element_by_xpath('//*[@id="AutoCode"]').click()
        time.sleep(2)
        stdin, stdout, stderr = ssh.exec_command("tail -n 100 /home/yscredit/tomcat/logs/ccb-riskEntry.log | grep 'SMSController'")
        shouji=(stdout.read().decode('utf-8'))
        result=re.findall(".*��֤�룺(.*)������.*",shouji)
        shoujiyanzhengma=str(result[len(result)-1])
        print(shoujiyanzhengma)
        #print(result)
        ssh.close()
        self.web.find_element_by_xpath('//*[@id="AutoCode2"]').send_keys(shoujiyanzhengma)  # �����ֻ���֤��
        self.web.find_element_by_xpath('//*[@id="applyFor%s"]'% applyid).click()    # ��½��ť1��2��3
        cookie_list=self.web.get_cookies()  # ��ȡcookie
        #print(cookie_list)
        cookie_dict=cookie_list[0]
        cookie={cookie_dict["name"]:cookie_dict["value"]}   # ��list��ȡ��name��value
        # print(cookie)
        time.sleep(2)
        global xcl_ent_adress
        xcl_ent_adress = []  # ����ȫ�ֱ����³�����ҵ��ַ��list
        global kjx_ent_adress
        kjx_ent_adress = []  # ����ȫ�ֱ����Ƽ�����ҵ��ַ��list
        global zdyq_ent_adress
        zdyq_ent_adress = []
        # ###�³���
        payload = {
            "type": "xcl",
            "pageSize": 10,
            "pageNum": 1
        }
        return_msg=json.loads(requests.get('https://ph-test.yscredit.com/risk/marketing/search',cookies=cookie,params=payload).text)    # ��������ת��json��ʽ
        if return_msg["obj"]["totalPage"] !=0:  # �ж��Ƿ�����������
            #print(return_msg)
            ent_list_obj=return_msg["obj"]

            for a in range(0,len(ent_list_obj['results'])): # ѭ��������Ϊ��ҳ�������
                ent_adress=ent_list_obj['results'][a]["regAddress"] # ȡ���³�����ҵ��ַ
                xcl_ent_adress.append(ent_adress)   # ��ӵ��³�����ҵ��ַlist
            #print(xcl_ent_adress)
            totalpage=ent_list_obj['totalPage']
            if totalpage>1:#�ж���ҳ������1
                for pagenum in range(2,totalpage+1):#�ӵڶ�ҳ��ʼѭ�������Ϊ���ҳ��
                    payload = {
                        "type": "xcl",
                        "pageSize": 10,
                        "pageNum": pagenum
                    }
                    return_msg=json.loads(requests.get('https://ph-test.yscredit.com/risk/marketing/search',cookies=cookie,params=payload).text)#��������ת��json��ʽ
                    ent_list_obj2=return_msg["obj"]
                    for adress in range(0,len(ent_list_obj2['results'])):
                        ent_adress=ent_list_obj2['results'][adress]["regAddress"]
                        xcl_ent_adress.append(ent_adress)
            #print(xcl_ent_adress)
        else:#��ҳ��С��1
            print("xcl_total=0")

        ####�Ƽ���
        payload = {
            "type": "kjx",
            "pageSize": 10,
            "pageNum": 1
        }
        return_msg=json.loads(requests.get('https://ph-test.yscredit.com/risk/marketing/search',cookies=cookie,params=payload).text)#��������ת��json��ʽ
        if return_msg["obj"]["totalPage"] !=0:#�ж��Ƿ�����������

            #print(return_msg)
            ent_list_obj=return_msg["obj"]
            for a in range(0,len(ent_list_obj['results'])):
                ent_adress=ent_list_obj['results'][a]["regAddress"]
                kjx_ent_adress.append(ent_adress)
            #print(kjx_ent_adress)
            totalpage=ent_list_obj['totalPage']
            if totalpage>1:
                for pagenum in range(2, totalpage+1):
                    payload = {
                        "type": "kjx",
                        "pageSize": 10,
                        "pageNum": pagenum
                    }
                    return_msg=json.loads(requests.get('https://ph-test.yscredit.com/risk/marketing/search',cookies=cookie,params=payload).text)
                    ent_list_obj2=return_msg["obj"]
                    for adress in range(0,len(ent_list_obj2['results'])):
                        ent_adress=ent_list_obj2['results'][adress]["regAddress"]
                        kjx_ent_adress.append(ent_adress)
            #print(kjx_ent_adress)
        else:
            print("kjx_total=0")

        ####�ص�԰��
        payload = {
            "type": "zdyq",
            "pageSize": 10,
            "pageNum": 1
        }
        return_msg=json.loads(requests.get('https://ph-test.yscredit.com/risk/marketing/search',cookies=cookie,params=payload).text)#��������ת��json��ʽ
        if return_msg["obj"]["totalPage"] != 0:

            #print(return_msg)
            ent_list_obj=return_msg["obj"]

            for a in range(0,len(ent_list_obj['results'])):
                ent_adress=ent_list_obj['results'][a]["regAddress"]
                zdyq_ent_adress.append(ent_adress)
            #print(kjx_ent_adress)
            totalpage=ent_list_obj['totalPage']
            if totalpage>1:
                for pagenum in range(2,totalpage+1):
                    payload = {
                        "type": "zdyq",
                        "pageSize": 10,
                        "pageNum": pagenum
                    }
                    return_msg=json.loads(requests.get('https://ph-test.yscredit.com/risk/marketing/search',cookies=cookie,params=payload).text)
                    ent_list_obj2=return_msg["obj"]
                    for adress in range(0,len(ent_list_obj2['results'])):
                        ent_adress=ent_list_obj2['results'][adress]["regAddress"]
                        zdyq_ent_adress.append(ent_adress)
            #print(zdyq_ent_adress)
        else:
            print("zdyq_total=0")

        #�ǳ�����
        username=self.web.find_element_by_xpath('//*[@id="user_name"]')
        ActionChains(self.web).move_to_element(username).perform()
        time.sleep(2)
        self.web.find_element_by_xpath('/html/body/div[1]/div[3]/span').click()


    def test_tangxi_11(self):
        self.login_in_phone('18000000011')#����֧��
        tangxi_rgpd=[]
        for entadress in xcl_ent_adress:
            if '�ຼ��������' not in entadress and '������̩ɽ��' not in entadress:
                tangxi_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '�ຼ��������' not in kjx_entadress and '������̩ɽ��' not in kjx_entadress:
                tangxi_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '�ຼ��������' not in zdyq_entadress and '������̩ɽ��' not in zdyq_entadress:
                tangxi_rgpd.append(zdyq_entadress)
        print(tangxi_rgpd)
        self.assertNotEqual(len(tangxi_rgpd),0)


    def test_liangzhu_12(self):
        self.login_in_phone('18000000012')
        liangzhu_rgpd=[]
        for entadress in xcl_ent_adress:
            if '��侽ֵ�' not in entadress:
                liangzhu_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '��侽ֵ�' not in kjx_entadress:
                liangzhu_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '��侽ֵ�' not in zdyq_entadress:
                liangzhu_rgpd.append(zdyq_entadress)

        print(liangzhu_rgpd)
        self.assertEqual(len(liangzhu_rgpd), 0)
    def test_lingping_13(self):
        self.login_in_phone('18000000013')
        lingping_rgpd=[]
        for entadress in xcl_ent_adress:
            if '��Է�ֵ�' in entadress:
                1==1
            else:
                lingping_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '��Է�ֵ�' in kjx_entadress:
                1==1
            else:
                lingping_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '��Է�ֵ�'  in zdyq_entadress:
                1==1
            else:
                lingping_rgpd.append(zdyq_entadress)

        print(lingping_rgpd)
        self.assertEqual(len(lingping_rgpd), 0)
    def test_pingyao_15(self):
        self.login_in_phone('18000000015')
        pingyao_rgpd=[]
        for entadress in xcl_ent_adress:
            if 'ƿҤ��' not in entadress and '�ųǴ�' not in entadress:
                pingyao_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress :
            if 'ƿҤ��' not in kjx_entadress and '�ųǴ�' not in kjx_entadress:
                pingyao_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if 'ƿҤ��' not in zdyq_entadress and '�ųǴ�' not in zdyq_entadress:
                pingyao_rgpd.append(zdyq_entadress)

        print(pingyao_rgpd)
        self.assertEqual(len(pingyao_rgpd), 0)
    def test_qiaosi_16(self):
        self.login_in_phone('18000000016')
        qiaosi_rgpd=[]
        for entadress in xcl_ent_adress:
            if '��˾�ֵ�' not in entadress and '��Է�ֵ�'not in entadress:
                qiaosi_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '��˾�ֵ�' not in kjx_entadress and '��Է�ֵ�'not in kjx_entadress:
                qiaosi_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress :
            if '��˾�ֵ�' not in zdyq_entadress and '��Է�ֵ�'not in zdyq_entadress:
                qiaosi_rgpd.append(zdyq_entadress)

        print(qiaosi_rgpd)
        self.assertEqual(len(qiaosi_rgpd), 0)
    def test_dongfang_17(self):#��ȷ��
        self.login_in_phone('18000000017')
        dongfang_rgpd=[]
        for entadress in xcl_ent_adress:
            if '�����ֵ�' not in entadress and '��ƽ�ֵ�'not in entadress:
                dongfang_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '�����ֵ�' not in kjx_entadress and '��ƽ�ֵ�'not in kjx_entadress:
                dongfang_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress :
            if '�����ֵ�' not in zdyq_entadress and '��ƽ�ֵ�'not in zdyq_entadress:
                dongfang_rgpd.append(zdyq_entadress)

        print(dongfang_rgpd)
        self.assertEqual(len(dongfang_rgpd), 0)
    def test_xingqiao_18(self):
        self.login_in_phone('18000000018')
        xingqiao_rgpd=[]
        for entadress in xcl_ent_adress:
            if '���Žֵ�' not in entadress and '�ж��Ƽ���' not in entadress and '��÷·' not in entadress:
                xingqiao_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '���Žֵ�' not in kjx_entadress and '�ж��Ƽ���' not in kjx_entadress and '��÷·' not in kjx_entadress:
                xingqiao_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '���Žֵ�' not in zdyq_entadress and '�ж��Ƽ���' not in zdyq_entadress and '��÷·' not in zdyq_entadress:
                xingqiao_rgpd.append(zdyq_entadress)

        print(xingqiao_rgpd)
        self.assertEqual(len(xingqiao_rgpd), 0)
    def test_liancheng_19(self):
        self.login_in_phone('18000000019')
        liancheng_rgpd=[]
        for entadress in xcl_ent_adress:
            if '��侽ֵ�' not in entadress:
                liancheng_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '��侽ֵ�' not in kjx_entadress:
                liancheng_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '��侽ֵ�' not in zdyq_entadress:
                liancheng_rgpd.append(zdyq_entadress)

        print(liancheng_rgpd)
        self.assertEqual(len(liancheng_rgpd), 0)
    def test_xixi_20(self):
        self.login_in_phone('18000000020')
        xixi_rgpd=[]
        for entadress in xcl_ent_adress:
            if '�峣���' not in entadress and '����' not in entadress and '��ɽ·' not in entadress \
                    and '���Ҿӳ�' not in entadress and '����·' not in entadress and '����·' not in entadress \
                    and '���Ǵ��Է' not in entadress:
                xixi_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '�峣���' not in kjx_entadress and '����' not in kjx_entadress and '��ɽ·' not in kjx_entadress \
                    and '���Ҿӳ�' not in kjx_entadress and '����·' not in kjx_entadress and '����·' not in kjx_entadress \
                    and '���Ǵ��Է' not in kjx_entadress:
                xixi_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress :
            if '�峣���' not in zdyq_entadress and '����' not in zdyq_entadress and '��ɽ·' not in zdyq_entadress \
                    and '���Ҿӳ�' not in zdyq_entadress and '����·' not in zdyq_entadress and '����·' not in zdyq_entadress \
                    and '���Ǵ��Է' not in zdyq_entadress:
                xixi_rgpd.append(zdyq_entadress)

        print(xixi_rgpd)
        self.assertEqual(len(xixi_rgpd), 0)
    def test_xianling_21(self):
        self.login_in_phone('18000000021')
        xianling_rgpd=[]
        for entadress in xcl_ent_adress:
            if '�峣�ֵ��峣���' not in entadress and '���ֵֽ�' not in entadress and '��ǰ�ֵ��μ�ɽ��' not in entadress \
                    and '���ֶ�·' not in entadress and '�Ϻ�·' not in entadress and '����·' not in entadress:
                xianling_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '�峣�ֵ��峣���' not in kjx_entadress and '���ֵֽ�' not in kjx_entadress and '��ǰ�ֵ��μ�ɽ��' not in kjx_entadress \
                    and '���ֶ�·' not in kjx_entadress and '�Ϻ�·' not in kjx_entadress and '����·' not in kjx_entadress:
                xianling_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '�峣�ֵ��峣���' not in zdyq_entadress and '���ֵֽ�' not in zdyq_entadress and '��ǰ�ֵ��μ�ɽ��' not in zdyq_entadress \
                    and '���ֶ�·' not in zdyq_entadress and '�Ϻ�·' not in zdyq_entadress and '����·' not in zdyq_entadress:
                xianling_rgpd.append(zdyq_entadress)

        print(xianling_rgpd)
        self.assertEqual(len(xianling_rgpd),0)
    def test_gouzhuang_22(self):
        self.login_in_phone('18000000022')
        gouzhuang_rgpd=[]
        for entadress in xcl_ent_adress:
            if '�ʺͽֵ�' not in entadress and '���ͽֵ��˺�·'not in entadress and '����·'not in entadress \
                    and '��԰·' not in entadress and '��侽ֵ����˽�' not in entadress and '���˺�·' not in entadress \
                    and '���˽�' not in entadress and '��ʢ·' not in entadress:
                gouzhuang_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '�ʺͽֵ�' not in kjx_entadress and '���ͽֵ��˺�·'not in kjx_entadress and '����·'not in kjx_entadress \
                    and '��԰·' not in kjx_entadress and '��侽ֵ����˽�' not in kjx_entadress and '���˺�·' not in kjx_entadress \
                    and '���˽�' not in kjx_entadress and '��ʢ·' not in kjx_entadress:
                gouzhuang_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '�ʺͽֵ�' not in zdyq_entadress and '���ͽֵ��˺�·'not in zdyq_ent_adress and '����·'not in zdyq_ent_adress \
                    and '��԰·' not in zdyq_ent_adress and '��侽ֵ����˽�' not in zdyq_ent_adress and '���˺�·' not in zdyq_ent_adress \
                    and '���˽�' not in zdyq_ent_adress and '��ʢ·' not in zdyq_ent_adress:
                gouzhuang_rgpd.append(zdyq_entadress)

        print(gouzhuang_rgpd)
        self.assertEqual(len(gouzhuang_rgpd), 0)
    def test_taiyan_23(self):
        self.login_in_phone('18000000023')
        taiyan_rgpd=[]
        for entadress in xcl_ent_adress:
            if '��̩�ֵ�' not in entadress and '��һ��·'not in entadress and '�ٻ�����' not in entadress \
                    and '�ຼ�ֵ�ʤ��·' not in entadress and '�ຼ�ֵ����̳�' not in entadress and '��һ·' not in entadress\
                    and '���ִ�' not in entadress and '��Ȫ·' not in entadress and '��̶·' not in entadress and '�Ƕ�·' not in entadress \
                    and '��ͩ��' not in entadress and '���Ǵ�' not in entadress and '����·' not in entadress and '���·' not in entadress:
                taiyan_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '��̩�ֵ�' not in kjx_entadress and '��һ��·'not in kjx_entadress and '�ٻ�����' not in kjx_entadress \
                    and '�ຼ�ֵ�ʤ��·' not in kjx_entadress and '�ຼ�ֵ����̳�' not in kjx_entadress and '��һ·' not in kjx_entadress \
                    and '���ִ�' not in kjx_entadress and '��Ȫ·' not in kjx_entadress and '��̶·' not in kjx_entadress and '�Ƕ�·' not in kjx_entadress \
                    and '��ͩ��' not in kjx_entadress and '���Ǵ�' not in kjx_entadress and '����·' not in kjx_entadress and '���·' not in kjx_entadress:
                taiyan_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '��̩�ֵ�' not in zdyq_entadress and '��һ��·' not in zdyq_entadress and '�ٻ�����' not in zdyq_entadress \
                    and '�ຼ�ֵ�ʤ��·' not in zdyq_entadress and '�ຼ�ֵ����̳�' not in zdyq_entadress and '��һ·' not in zdyq_entadress \
                    and '���ִ�' not in zdyq_entadress and '��Ȫ·' not in zdyq_entadress and '��̶·' not in zdyq_entadress and '�Ƕ�·' not in zdyq_entadress \
                    and '��ͩ��' not in zdyq_entadress and '���Ǵ�' not in zdyq_entadress and '����·' not in zdyq_entadress and '���·' not in zdyq_entadress:
                taiyan_rgpd.append(zdyq_entadress)

        print(taiyan_rgpd)
        self.assertEqual(len(taiyan_rgpd), 0)
    def test_yuhang_24(self):
        self.login_in_phone('18000000024')
        yuhang_rgpd=[]
        for entadress in xcl_ent_adress:
            if '��ƽ�ֵ�' not in entadress and '�����ֵ�'not in entadress and '���˶�·'not in entadress and '�˹�·' not in entadress\
                    and '���˶�·' not in entadress and '���·' not in entadress and '���·' not in entadress and '������·' not in entadress \
                    and '��ɳ��·' not in entadress and '��Ԫ·' not in entadress and '���嶫·' not in entadress and '����·' not in entadress \
                    and '��ɳ��·' not in entadress and '���·' not in entadress:
                yuhang_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '��ƽ�ֵ�' not in kjx_entadress and '�����ֵ�'not in kjx_entadress and '���˶�·'not in kjx_entadress and '�˹�·' not in kjx_entadress\
                    and '���˶�·' not in kjx_entadress and '���·' not in kjx_entadress and '���·' not in kjx_entadress and '������·' not in kjx_entadress \
                    and '��ɳ��·' not in kjx_entadress and '��Ԫ·' not in kjx_entadress and '���嶫·' not in kjx_entadress and '����·' not in kjx_entadress \
                    and '��ɳ��·' not in kjx_entadress and '���·' not in kjx_entadress:
                yuhang_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress :
            if '��ƽ�ֵ�' not in zdyq_entadress and '�����ֵ�'not in zdyq_entadress and '���˶�·'not in zdyq_entadress and '�˹�·' not in zdyq_entadress\
                    and '���˶�·' not in zdyq_entadress and '���·' not in zdyq_entadress and '���·' not in zdyq_entadress and '������·' not in zdyq_entadress \
                    and '��ɳ��·' not in zdyq_entadress and '��Ԫ·' not in zdyq_entadress and '���嶫·' not in zdyq_entadress and '����·' not in zdyq_entadress \
                    and '��ɳ��·' not in zdyq_entadress and '���·' not in zdyq_entadress:
                yuhang_rgpd.append(zdyq_entadress)

        print(yuhang_rgpd)
        self.assertEqual(len(yuhang_rgpd), 0)
    def test_chengbei_25(self):
        self.login_in_phone('18000000025')
        chengbei_rgpd=[]
        for entadress in xcl_ent_adress:
            if '���ÿ�����' not in entadress and '�ຼ��Ǯ�����ÿ�����'not in entadress \
                    and '��ƽ���'not in entadress and '����Ǯ�����ʴ���' not in entadress \
                    and '���ϴ�' not in entadress and '����·' not in entadress and '�����ֵ�' not in entadress \
                    and '����·' not in entadress and '˳��·' not in entadress and '����·' not in entadress and '����·' not in entadress \
                    and '�˺ӽֵ����´�' not in entadress and '�Ϲ���·' not in entadress and '����·' not in entadress and '��ƽ�ֵ�' not in entadress \
                    and '����·' not in entadress and '������·' not in entadress and '����·' not in entadress \
                    and '��˿·' not in entadress and '˳��·' not in entadress \
                    and '����·' not in entadress and '���·' not in entadress and '�Ϲ���·' not in entadress \
                    and '����·' not in entadress and 'ֺͤ��' not in entadress and '�����ֵ���������' not in entadress \
                    and '̩��·' not in entadress  and '�˺ӽֵ���Ҷ�' not in entadress and '����·511��' not in entadress:
                chengbei_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '���ÿ�����' not in kjx_entadress and '�ຼ��Ǯ�����ÿ�����'not in kjx_entadress \
                    and '��ƽ���'not in kjx_entadress and '����Ǯ�����ʴ���' not in kjx_entadress \
                    and '���ϴ�' not in kjx_entadress and '����·' not in kjx_entadress and '�����ֵ�' not in kjx_entadress \
                    and '����·' not in kjx_entadress and '˳��·' not in kjx_entadress and '����·' not in kjx_entadress and '����·' not in kjx_entadress \
                    and '�˺ӽֵ����´�' not in kjx_entadress and '�Ϲ���·' not in kjx_entadress and '����·' not in kjx_entadress and '��ƽ�ֵ�' not in kjx_entadress \
                    and '����·' not in kjx_entadress and '������·' not in kjx_entadress and '����·' not in kjx_entadress \
                    and '��˿·' not in kjx_entadress and '˳��·' not in kjx_entadress \
                    and '����·' not in kjx_entadress and '���·' not in kjx_entadress and '�Ϲ���·' not in kjx_entadress \
                    and '����·' not in kjx_entadress and 'ֺͤ��' not in kjx_entadress and '�����ֵ���������' not in kjx_entadress \
                    and '̩��·' not in kjx_entadress  and '�˺ӽֵ���Ҷ�' not in kjx_entadress and '����·511��' not in kjx_entadress:
                chengbei_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '���ÿ�����' not in zdyq_entadress and '�ຼ��Ǯ�����ÿ�����' not in zdyq_entadress \
                    and '��ƽ���' not in zdyq_entadress and '����Ǯ�����ʴ���' not in zdyq_entadress \
                    and '���ϴ�' not in zdyq_entadress and '����·' not in zdyq_entadress and '�����ֵ�' not in zdyq_entadress \
                    and '����·' not in zdyq_entadress and '˳��·' not in zdyq_entadress and '����·' not in zdyq_entadress and '����·' not in zdyq_entadress \
                    and '�˺ӽֵ����´�' not in zdyq_entadress and '�Ϲ���·' not in zdyq_entadress and '����·' not in zdyq_entadress and '��ƽ�ֵ�' not in zdyq_entadress \
                    and '����·' not in zdyq_entadress and '������·' not in zdyq_entadress and '����·' not in zdyq_entadress \
                    and '��˿·' not in zdyq_entadress and '˳��·' not in zdyq_entadress \
                    and '����·' not in zdyq_entadress and '���·' not in zdyq_entadress and '�Ϲ���·' not in zdyq_entadress \
                    and '����·' not in zdyq_entadress and 'ֺͤ��' not in zdyq_entadress and '�����ֵ���������' not in zdyq_entadress \
                    and '̩��·' not in zdyq_entadress  and '�˺ӽֵ���Ҷ�' not in zdyq_entadress and '����·511��' not in zdyq_entadress:
                chengbei_rgpd.append(zdyq_entadress)

        print(chengbei_rgpd)
        self.assertEqual(len(chengbei_rgpd), 0)
    def test_chongxian_26(self):
        self.login_in_phone('18000000026')
        chongxian_rgpd=[]
        for entadress in xcl_ent_adress:
            if '���ͽֵ�' not in entadress and '̩ɽ��' not in entadress:
                chongxian_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '���ͽֵ�' not in kjx_entadress and '̩ɽ��' not in kjx_entadress:
                chongxian_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '���ͽֵ�' not in zdyq_entadress and '̩ɽ��' not in zdyq_entadress:
                chongxian_rgpd.append(zdyq_entadress)

        print(chongxian_rgpd)
        self.assertEqual(len(chongxian_rgpd), 0)
    def test_chengxi_27(self):
        self.login_in_phone('18000000027')
        chengxi_rgpd=[]
        for entadress in xcl_ent_adress:
            if '��Ϫ' not in entadress and '��ǰ�ֵ�'not in entadress and '��һ��·'not in entadress \
                    and 'ʢ������' not in entadress and '�������' not in entadress and '��Խ�̹�����' not in entadress \
                    and '��������' not in entadress and '�������' not in entadress and '������' not in entadress and '�峣�ֵ�������' not in entadress \
                    and '��һ����' not in entadress and '�߽�·' not in entadress and '����������������' not in entadress and '����·' not in entadress:
                chengxi_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '��Ϫ' not in kjx_entadress and '��ǰ�ֵ�'not in kjx_entadress and '��һ��·'not in kjx_entadress \
                    and 'ʢ������' not in kjx_entadress and '�������' not in kjx_entadress and '��Խ�̹�����' not in kjx_entadress \
                    and '��������' not in kjx_entadress and '�������' not in kjx_entadress and '������' not in kjx_entadress and '�峣�ֵ�������' not in kjx_entadress \
                    and '��һ����' not in kjx_entadress and '�߽�·' not in kjx_entadress and '����������������' not in kjx_entadress and '����·' not in kjx_entadress:
                chengxi_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '��Ϫ' not in zdyq_entadress and '��ǰ�ֵ�'not in zdyq_entadress and '��һ��·'not in zdyq_entadress \
                  and 'ʢ������' not in zdyq_entadress and '�������' not in zdyq_entadress and '��Խ�̹�����' not in zdyq_entadress \
                  and '��������' not in zdyq_entadress and '�������' not in zdyq_entadress and '������' not in zdyq_entadress and '�峣�ֵ�������' not in zdyq_entadress \
                    and '��һ����' not in zdyq_entadress and '�߽�·' not in zdyq_entadress and '����������������' not in zdyq_entadress and '����·' not in zdyq_entadress:
                chengxi_rgpd.append(zdyq_entadress)

        print(chengxi_rgpd)
        self.assertEqual(len(chengxi_rgpd), 0)
    def test_linpingxingcheng_28(self):
        self.login_in_phone('18000000028')
        linpingxingcheng_rgpd=[]
        for entadress in xcl_ent_adress:
            if '��Է�ֵ�' not in entadress:
                linpingxingcheng_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '��Է�ֵ�' not in kjx_entadress:
                linpingxingcheng_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '��Է�ֵ�' not in zdyq_entadress:
                linpingxingcheng_rgpd.append(zdyq_entadress)
        print(linpingxingcheng_rgpd)
        self.assertEqual(len(linpingxingcheng_rgpd), 0)