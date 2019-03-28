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
    def login_in_phone(self,phonenum,user='toggleCenter',applyid='3'):#toggleLeft、toggleCenter、toggleRight
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
        time.sleep(2)
        stdin, stdout, stderr = ssh.exec_command("tail -n 100 /home/yscredit/tomcat/logs/ccb-riskEntry.log | grep 'SMSController'")
        shouji=(stdout.read().decode('utf-8'))
        result=re.findall(".*验证码：(.*)，请在.*",shouji)
        shoujiyanzhengma=str(result[len(result)-1])
        print(shoujiyanzhengma)
        #print(result)
        ssh.close()
        self.web.find_element_by_xpath('//*[@id="AutoCode2"]').send_keys(shoujiyanzhengma)  # 输入手机验证码
        self.web.find_element_by_xpath('//*[@id="applyFor%s"]'% applyid).click()    # 登陆按钮1、2、3
        cookie_list=self.web.get_cookies()  # 获取cookie
        #print(cookie_list)
        cookie_dict=cookie_list[0]
        cookie={cookie_dict["name"]:cookie_dict["value"]}   # 从list中取出name和value
        # print(cookie)
        time.sleep(2)
        global xcl_ent_adress
        xcl_ent_adress = []  # 定义全局变量新成立企业地址的list
        global kjx_ent_adress
        kjx_ent_adress = []  # 定义全局变量科技型企业地址的list
        global zdyq_ent_adress
        zdyq_ent_adress = []
        # ###新成立
        payload = {
            "type": "xcl",
            "pageSize": 10,
            "pageNum": 1
        }
        return_msg=json.loads(requests.get('https://ph-test.yscredit.com/risk/marketing/search',cookies=cookie,params=payload).text)    # 发送请求并转成json格式
        if return_msg["obj"]["totalPage"] !=0:  # 判断是否有数据推送
            #print(return_msg)
            ent_list_obj=return_msg["obj"]

            for a in range(0,len(ent_list_obj['results'])): # 循环最大次数为单页最大条数
                ent_adress=ent_list_obj['results'][a]["regAddress"] # 取出新成立企业地址
                xcl_ent_adress.append(ent_adress)   # 添加到新成立企业地址list
            #print(xcl_ent_adress)
            totalpage=ent_list_obj['totalPage']
            if totalpage>1:#判断总页数大于1
                for pagenum in range(2,totalpage+1):#从第二页开始循环，最大为最大页数
                    payload = {
                        "type": "xcl",
                        "pageSize": 10,
                        "pageNum": pagenum
                    }
                    return_msg=json.loads(requests.get('https://ph-test.yscredit.com/risk/marketing/search',cookies=cookie,params=payload).text)#发送请求并转成json格式
                    ent_list_obj2=return_msg["obj"]
                    for adress in range(0,len(ent_list_obj2['results'])):
                        ent_adress=ent_list_obj2['results'][adress]["regAddress"]
                        xcl_ent_adress.append(ent_adress)
            #print(xcl_ent_adress)
        else:#总页数小于1
            print("xcl_total=0")

        ####科技型
        payload = {
            "type": "kjx",
            "pageSize": 10,
            "pageNum": 1
        }
        return_msg=json.loads(requests.get('https://ph-test.yscredit.com/risk/marketing/search',cookies=cookie,params=payload).text)#发送请求并转成json格式
        if return_msg["obj"]["totalPage"] !=0:#判断是否有数据推送

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

        ####重点园区
        payload = {
            "type": "zdyq",
            "pageSize": 10,
            "pageNum": 1
        }
        return_msg=json.loads(requests.get('https://ph-test.yscredit.com/risk/marketing/search',cookies=cookie,params=payload).text)#发送请求并转成json格式
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

        #登出操作
        username=self.web.find_element_by_xpath('//*[@id="user_name"]')
        ActionChains(self.web).move_to_element(username).perform()
        time.sleep(2)
        self.web.find_element_by_xpath('/html/body/div[1]/div[3]/span').click()


    def test_tangxi_11(self):
        self.login_in_phone('18000000011')#塘西支行
        tangxi_rgpd=[]
        for entadress in xcl_ent_adress:
            if '余杭区塘栖镇' not in entadress and '塘栖镇泰山村' not in entadress:
                tangxi_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '余杭区塘栖镇' not in kjx_entadress and '塘栖镇泰山村' not in kjx_entadress:
                tangxi_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '余杭区塘栖镇' not in zdyq_entadress and '塘栖镇泰山村' not in zdyq_entadress:
                tangxi_rgpd.append(zdyq_entadress)
        print(tangxi_rgpd)
        self.assertNotEqual(len(tangxi_rgpd),0)


    def test_liangzhu_12(self):
        self.login_in_phone('18000000012')
        liangzhu_rgpd=[]
        for entadress in xcl_ent_adress:
            if '良渚街道' not in entadress:
                liangzhu_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '良渚街道' not in kjx_entadress:
                liangzhu_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '良渚街道' not in zdyq_entadress:
                liangzhu_rgpd.append(zdyq_entadress)

        print(liangzhu_rgpd)
        self.assertEqual(len(liangzhu_rgpd), 0)
    def test_lingping_13(self):
        self.login_in_phone('18000000013')
        lingping_rgpd=[]
        for entadress in xcl_ent_adress:
            if '南苑街道' in entadress:
                1==1
            else:
                lingping_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '南苑街道' in kjx_entadress:
                1==1
            else:
                lingping_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '南苑街道'  in zdyq_entadress:
                1==1
            else:
                lingping_rgpd.append(zdyq_entadress)

        print(lingping_rgpd)
        self.assertEqual(len(lingping_rgpd), 0)
    def test_pingyao_15(self):
        self.login_in_phone('18000000015')
        pingyao_rgpd=[]
        for entadress in xcl_ent_adress:
            if '瓶窑镇' not in entadress and '杜城村' not in entadress:
                pingyao_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress :
            if '瓶窑镇' not in kjx_entadress and '杜城村' not in kjx_entadress:
                pingyao_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '瓶窑镇' not in zdyq_entadress and '杜城村' not in zdyq_entadress:
                pingyao_rgpd.append(zdyq_entadress)

        print(pingyao_rgpd)
        self.assertEqual(len(pingyao_rgpd), 0)
    def test_qiaosi_16(self):
        self.login_in_phone('18000000016')
        qiaosi_rgpd=[]
        for entadress in xcl_ent_adress:
            if '乔司街道' not in entadress and '南苑街道'not in entadress:
                qiaosi_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '乔司街道' not in kjx_entadress and '南苑街道'not in kjx_entadress:
                qiaosi_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress :
            if '乔司街道' not in zdyq_entadress and '南苑街道'not in zdyq_entadress:
                qiaosi_rgpd.append(zdyq_entadress)

        print(qiaosi_rgpd)
        self.assertEqual(len(qiaosi_rgpd), 0)
    def test_dongfang_17(self):#待确定
        self.login_in_phone('18000000017')
        dongfang_rgpd=[]
        for entadress in xcl_ent_adress:
            if '东湖街道' not in entadress and '临平街道'not in entadress:
                dongfang_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '东湖街道' not in kjx_entadress and '临平街道'not in kjx_entadress:
                dongfang_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress :
            if '东湖街道' not in zdyq_entadress and '临平街道'not in zdyq_entadress:
                dongfang_rgpd.append(zdyq_entadress)

        print(dongfang_rgpd)
        self.assertEqual(len(dongfang_rgpd), 0)
    def test_xingqiao_18(self):
        self.login_in_phone('18000000018')
        xingqiao_rgpd=[]
        for entadress in xcl_ent_adress:
            if '星桥街道' not in entadress and '谛都科技城' not in entadress and '唐梅路' not in entadress:
                xingqiao_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '星桥街道' not in kjx_entadress and '谛都科技城' not in kjx_entadress and '唐梅路' not in kjx_entadress:
                xingqiao_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '星桥街道' not in zdyq_entadress and '谛都科技城' not in zdyq_entadress and '唐梅路' not in zdyq_entadress:
                xingqiao_rgpd.append(zdyq_entadress)

        print(xingqiao_rgpd)
        self.assertEqual(len(xingqiao_rgpd), 0)
    def test_liancheng_19(self):
        self.login_in_phone('18000000019')
        liancheng_rgpd=[]
        for entadress in xcl_ent_adress:
            if '良渚街道' not in entadress:
                liancheng_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '良渚街道' not in kjx_entadress:
                liancheng_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '良渚街道' not in zdyq_entadress:
                liancheng_rgpd.append(zdyq_entadress)

        print(liancheng_rgpd)
        self.assertEqual(len(liancheng_rgpd), 0)
    def test_xixi_20(self):
        self.login_in_phone('18000000020')
        xixi_rgpd=[]
        for entadress in xcl_ent_adress:
            if '五常大道' not in entadress and '辅助' not in entadress and '后山路' not in entadress \
                    and '宏丰家居城' not in entadress and '丰岭路' not in entadress and '荆长路' not in entadress \
                    and '翡翠城翠湖苑' not in entadress:
                xixi_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '五常大道' not in kjx_entadress and '辅助' not in kjx_entadress and '后山路' not in kjx_entadress \
                    and '宏丰家居城' not in kjx_entadress and '丰岭路' not in kjx_entadress and '荆长路' not in kjx_entadress \
                    and '翡翠城翠湖苑' not in kjx_entadress:
                xixi_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress :
            if '五常大道' not in zdyq_entadress and '辅助' not in zdyq_entadress and '后山路' not in zdyq_entadress \
                    and '宏丰家居城' not in zdyq_entadress and '丰岭路' not in zdyq_entadress and '荆长路' not in zdyq_entadress \
                    and '翡翠城翠湖苑' not in zdyq_entadress:
                xixi_rgpd.append(zdyq_entadress)

        print(xixi_rgpd)
        self.assertEqual(len(xixi_rgpd), 0)
    def test_xianling_21(self):
        self.login_in_phone('18000000021')
        xianling_rgpd=[]
        for entadress in xcl_ent_adress:
            if '五常街道五常大道' not in entadress and '闲林街道' not in entadress and '仓前街道宋家山村' not in entadress \
                    and '闲林东路' not in entadress and '上和路' not in entadress and '荆余路' not in entadress:
                xianling_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '五常街道五常大道' not in kjx_entadress and '闲林街道' not in kjx_entadress and '仓前街道宋家山村' not in kjx_entadress \
                    and '闲林东路' not in kjx_entadress and '上和路' not in kjx_entadress and '荆余路' not in kjx_entadress:
                xianling_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '五常街道五常大道' not in zdyq_entadress and '闲林街道' not in zdyq_entadress and '仓前街道宋家山村' not in zdyq_entadress \
                    and '闲林东路' not in zdyq_entadress and '上和路' not in zdyq_entadress and '荆余路' not in zdyq_entadress:
                xianling_rgpd.append(zdyq_entadress)

        print(xianling_rgpd)
        self.assertEqual(len(xianling_rgpd),0)
    def test_gouzhuang_22(self):
        self.login_in_phone('18000000022')
        gouzhuang_rgpd=[]
        for entadress in xcl_ent_adress:
            if '仁和街道' not in entadress and '崇贤街道运河路'not in entadress and '拱康路'not in entadress \
                    and '博园路' not in entadress and '良渚街道好运街' not in entadress and '古运河路' not in entadress \
                    and '良运街' not in entadress and '逸盛路' not in entadress:
                gouzhuang_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '仁和街道' not in kjx_entadress and '崇贤街道运河路'not in kjx_entadress and '拱康路'not in kjx_entadress \
                    and '博园路' not in kjx_entadress and '良渚街道好运街' not in kjx_entadress and '古运河路' not in kjx_entadress \
                    and '良运街' not in kjx_entadress and '逸盛路' not in kjx_entadress:
                gouzhuang_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '仁和街道' not in zdyq_entadress and '崇贤街道运河路'not in zdyq_ent_adress and '拱康路'not in zdyq_ent_adress \
                    and '博园路' not in zdyq_ent_adress and '良渚街道好运街' not in zdyq_ent_adress and '古运河路' not in zdyq_ent_adress \
                    and '良运街' not in zdyq_ent_adress and '逸盛路' not in zdyq_ent_adress:
                gouzhuang_rgpd.append(zdyq_entadress)

        print(gouzhuang_rgpd)
        self.assertEqual(len(gouzhuang_rgpd), 0)
    def test_taiyan_23(self):
        self.login_in_phone('18000000023')
        taiyan_rgpd=[]
        for entadress in xcl_ent_adress:
            if '中泰街道' not in entadress and '文一西路'not in entadress and '百汇中心' not in entadress \
                    and '余杭街道胜义路' not in entadress and '余杭街道禹航商城' not in entadress and '华一路' not in entadress\
                    and '永乐村' not in entadress and '龙泉路' not in entadress and '龙潭路' not in entadress and '城东路' not in entadress \
                    and '洪桐村' not in entadress and '金星村' not in entadress and '海曙路' not in entadress and '余昌路' not in entadress:
                taiyan_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '中泰街道' not in kjx_entadress and '文一西路'not in kjx_entadress and '百汇中心' not in kjx_entadress \
                    and '余杭街道胜义路' not in kjx_entadress and '余杭街道禹航商城' not in kjx_entadress and '华一路' not in kjx_entadress \
                    and '永乐村' not in kjx_entadress and '龙泉路' not in kjx_entadress and '龙潭路' not in kjx_entadress and '城东路' not in kjx_entadress \
                    and '洪桐村' not in kjx_entadress and '金星村' not in kjx_entadress and '海曙路' not in kjx_entadress and '余昌路' not in kjx_entadress:
                taiyan_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '中泰街道' not in zdyq_entadress and '文一西路' not in zdyq_entadress and '百汇中心' not in zdyq_entadress \
                    and '余杭街道胜义路' not in zdyq_entadress and '余杭街道禹航商城' not in zdyq_entadress and '华一路' not in zdyq_entadress \
                    and '永乐村' not in zdyq_entadress and '龙泉路' not in zdyq_entadress and '龙潭路' not in zdyq_entadress and '城东路' not in zdyq_entadress \
                    and '洪桐村' not in zdyq_entadress and '金星村' not in zdyq_entadress and '海曙路' not in zdyq_entadress and '余昌路' not in zdyq_entadress:
                taiyan_rgpd.append(zdyq_entadress)

        print(taiyan_rgpd)
        self.assertEqual(len(taiyan_rgpd), 0)
    def test_yuhang_24(self):
        self.login_in_phone('18000000024')
        yuhang_rgpd=[]
        for entadress in xcl_ent_adress:
            if '临平街道' not in entadress and '东湖街道'not in entadress and '振兴东路'not in entadress and '兴国路' not in entadress\
                    and '振兴东路' not in entadress and '红丰路' not in entadress and '宏达路' not in entadress and '东湖北路' not in entadress \
                    and '北沙东路' not in entadress and '兴元路' not in entadress and '超峰东路' not in entadress and '五洲路' not in entadress \
                    and '北沙西路' not in entadress and '天荷路' not in entadress:
                yuhang_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '临平街道' not in kjx_entadress and '东湖街道'not in kjx_entadress and '振兴东路'not in kjx_entadress and '兴国路' not in kjx_entadress\
                    and '振兴东路' not in kjx_entadress and '红丰路' not in kjx_entadress and '宏达路' not in kjx_entadress and '东湖北路' not in kjx_entadress \
                    and '北沙东路' not in kjx_entadress and '兴元路' not in kjx_entadress and '超峰东路' not in kjx_entadress and '五洲路' not in kjx_entadress \
                    and '北沙西路' not in kjx_entadress and '天荷路' not in kjx_entadress:
                yuhang_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress :
            if '临平街道' not in zdyq_entadress and '东湖街道'not in zdyq_entadress and '振兴东路'not in zdyq_entadress and '兴国路' not in zdyq_entadress\
                    and '振兴东路' not in zdyq_entadress and '红丰路' not in zdyq_entadress and '宏达路' not in zdyq_entadress and '东湖北路' not in zdyq_entadress \
                    and '北沙东路' not in zdyq_entadress and '兴元路' not in zdyq_entadress and '超峰东路' not in zdyq_entadress and '五洲路' not in zdyq_entadress \
                    and '北沙西路' not in zdyq_entadress and '天荷路' not in zdyq_entadress:
                yuhang_rgpd.append(zdyq_entadress)

        print(yuhang_rgpd)
        self.assertEqual(len(yuhang_rgpd), 0)
    def test_chengbei_25(self):
        self.login_in_phone('18000000025')
        chengbei_rgpd=[]
        for entadress in xcl_ent_adress:
            if '经济开发区' not in entadress and '余杭区钱江经济开发区'not in entadress \
                    and '临平大道'not in entadress and '欣北钱江国际大厦' not in entadress \
                    and '杭南村' not in entadress and '万年路' not in entadress and '东湖街道' not in entadress \
                    and '华宁路' not in entadress and '顺风路' not in entadress and '新天路' not in entadress and '塘宁路' not in entadress \
                    and '运河街道东新村' not in entadress and '南公河路' not in entadress and '费兴路' not in entadress and '临平街道' not in entadress \
                    and '达与路' not in entadress and '东湖北路' not in entadress and '昌达路' not in entadress \
                    and '新丝路' not in entadress and '顺风路' not in entadress \
                    and '五洲路' not in entadress and '宏达路' not in entadress and '南公河路' not in entadress \
                    and '新颜路' not in entadress and '亭趾村' not in entadress and '东湖街道新塘社区' not in entadress \
                    and '泰极路' not in entadress  and '运河街道杨家墩' not in entadress and '兴中路511号' not in entadress:
                chengbei_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '经济开发区' not in kjx_entadress and '余杭区钱江经济开发区'not in kjx_entadress \
                    and '临平大道'not in kjx_entadress and '欣北钱江国际大厦' not in kjx_entadress \
                    and '杭南村' not in kjx_entadress and '万年路' not in kjx_entadress and '东湖街道' not in kjx_entadress \
                    and '华宁路' not in kjx_entadress and '顺风路' not in kjx_entadress and '新天路' not in kjx_entadress and '塘宁路' not in kjx_entadress \
                    and '运河街道东新村' not in kjx_entadress and '南公河路' not in kjx_entadress and '费兴路' not in kjx_entadress and '临平街道' not in kjx_entadress \
                    and '达与路' not in kjx_entadress and '东湖北路' not in kjx_entadress and '昌达路' not in kjx_entadress \
                    and '新丝路' not in kjx_entadress and '顺风路' not in kjx_entadress \
                    and '五洲路' not in kjx_entadress and '宏达路' not in kjx_entadress and '南公河路' not in kjx_entadress \
                    and '新颜路' not in kjx_entadress and '亭趾村' not in kjx_entadress and '东湖街道新塘社区' not in kjx_entadress \
                    and '泰极路' not in kjx_entadress  and '运河街道杨家墩' not in kjx_entadress and '兴中路511号' not in kjx_entadress:
                chengbei_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '经济开发区' not in zdyq_entadress and '余杭区钱江经济开发区' not in zdyq_entadress \
                    and '临平大道' not in zdyq_entadress and '欣北钱江国际大厦' not in zdyq_entadress \
                    and '杭南村' not in zdyq_entadress and '万年路' not in zdyq_entadress and '东湖街道' not in zdyq_entadress \
                    and '华宁路' not in zdyq_entadress and '顺风路' not in zdyq_entadress and '新天路' not in zdyq_entadress and '塘宁路' not in zdyq_entadress \
                    and '运河街道东新村' not in zdyq_entadress and '南公河路' not in zdyq_entadress and '费兴路' not in zdyq_entadress and '临平街道' not in zdyq_entadress \
                    and '达与路' not in zdyq_entadress and '东湖北路' not in zdyq_entadress and '昌达路' not in zdyq_entadress \
                    and '新丝路' not in zdyq_entadress and '顺风路' not in zdyq_entadress \
                    and '五洲路' not in zdyq_entadress and '宏达路' not in zdyq_entadress and '南公河路' not in zdyq_entadress \
                    and '新颜路' not in zdyq_entadress and '亭趾村' not in zdyq_entadress and '东湖街道新塘社区' not in zdyq_entadress \
                    and '泰极路' not in zdyq_entadress  and '运河街道杨家墩' not in zdyq_entadress and '兴中路511号' not in zdyq_entadress:
                chengbei_rgpd.append(zdyq_entadress)

        print(chengbei_rgpd)
        self.assertEqual(len(chengbei_rgpd), 0)
    def test_chongxian_26(self):
        self.login_in_phone('18000000026')
        chongxian_rgpd=[]
        for entadress in xcl_ent_adress:
            if '崇贤街道' not in entadress and '泰山村' not in entadress:
                chongxian_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '崇贤街道' not in kjx_entadress and '泰山村' not in kjx_entadress:
                chongxian_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '崇贤街道' not in zdyq_entadress and '泰山村' not in zdyq_entadress:
                chongxian_rgpd.append(zdyq_entadress)

        print(chongxian_rgpd)
        self.assertEqual(len(chongxian_rgpd), 0)
    def test_chengxi_27(self):
        self.login_in_phone('18000000027')
        chengxi_rgpd=[]
        for entadress in xcl_ent_adress:
            if '西溪' not in entadress and '仓前街道'not in entadress and '文一西路'not in entadress \
                    and '盛奥铭座' not in entadress and '瑞谷中心' not in entadress and '尚越绿谷中心' not in entadress \
                    and '万利大厦' not in entadress and '荆长大道' not in entadress and '向往街' not in entadress and '五常街道联创街' not in entadress \
                    and '文一社区' not in entadress and '高教路' not in entadress and '赛银国际商务中心' not in entadress and '良睦路' not in entadress:
                chengxi_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '西溪' not in kjx_entadress and '仓前街道'not in kjx_entadress and '文一西路'not in kjx_entadress \
                    and '盛奥铭座' not in kjx_entadress and '瑞谷中心' not in kjx_entadress and '尚越绿谷中心' not in kjx_entadress \
                    and '万利大厦' not in kjx_entadress and '荆长大道' not in kjx_entadress and '向往街' not in kjx_entadress and '五常街道联创街' not in kjx_entadress \
                    and '文一社区' not in kjx_entadress and '高教路' not in kjx_entadress and '赛银国际商务中心' not in kjx_entadress and '良睦路' not in kjx_entadress:
                chengxi_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '西溪' not in zdyq_entadress and '仓前街道'not in zdyq_entadress and '文一西路'not in zdyq_entadress \
                  and '盛奥铭座' not in zdyq_entadress and '瑞谷中心' not in zdyq_entadress and '尚越绿谷中心' not in zdyq_entadress \
                  and '万利大厦' not in zdyq_entadress and '荆长大道' not in zdyq_entadress and '向往街' not in zdyq_entadress and '五常街道联创街' not in zdyq_entadress \
                    and '文一社区' not in zdyq_entadress and '高教路' not in zdyq_entadress and '赛银国际商务中心' not in zdyq_entadress and '良睦路' not in zdyq_entadress:
                chengxi_rgpd.append(zdyq_entadress)

        print(chengxi_rgpd)
        self.assertEqual(len(chengxi_rgpd), 0)
    def test_linpingxingcheng_28(self):
        self.login_in_phone('18000000028')
        linpingxingcheng_rgpd=[]
        for entadress in xcl_ent_adress:
            if '南苑街道' not in entadress:
                linpingxingcheng_rgpd.append(entadress)
        for kjx_entadress in kjx_ent_adress:
            if '南苑街道' not in kjx_entadress:
                linpingxingcheng_rgpd.append(kjx_entadress)
        for zdyq_entadress in zdyq_ent_adress:
            if '南苑街道' not in zdyq_entadress:
                linpingxingcheng_rgpd.append(zdyq_entadress)
        print(linpingxingcheng_rgpd)
        self.assertEqual(len(linpingxingcheng_rgpd), 0)