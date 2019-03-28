import unittest

from selenium import webdriver

from config import config1

url=config1.get_login_msg.get_url()
cookie = config1.get_login_msg.get_cookie()
wlhk_table=config1.get_login_msg.get_wlhk_table()
all_entname_path=config1.get_wlhk_elm.get_xinchengliqiye_all_entname()
xingchengliqiye_one_entmsg=config1.get_wlhk_elm.get_xingchengliqiye_one_entmsg()
xingchengliqiye_linquchenggong_msg=config1.get_wlhk_elm.get_xingchengliqiye_linquchenggong_msg()
wdkh_table=config1.get_login_msg.get_wdkh_table()
wdkh_first_entname=config1.get_wdkh_elm.get_wdkh_first_entname()
zdyqqy_table=config1.get_wlhk_elm.get_zdyqqy_table()
zdyqqy_one_entmsg=config1.get_wlhk_elm.get_zfyqqy_one_entmsg()
zdyqqy_one_entname=config1.get_wlhk_elm.get_zdyqqy_one_entname()
zdyqqy_all_entname=config1.get_wlhk_elm.get_zdyqqy_all_entname()

class Weilanhuoke_lingqu(unittest.TestCase):
    def setUp(self):
        self.web=webdriver.Chrome()
        self.web.get(url)
        self.web.add_cookie(cookie)
        self.web.get(url)
        self.web.implicitly_wait(10)
    def tearDown(self):
        self.web.quit()
    def is_not_displayed(self,path):#元素是否存在判断方法
        flag=True
        try:
            self.web.find_element_by_xpath(path)
            flag=False
        except:
            print('elm is not displayed')
            flag=True
        return flag

    def weilanhuoke_lingqu(self,entname):
        self.web.find_element_by_xpath(wlhk_table).click()#点击围栏获客table
        self.web.find_element_by_xpath(zdyqqy_table).click()
        ent_list=self.web.find_elements_by_xpath(zdyqqy_all_entname)#找到第一页所有企业
        ent_list_len = len(ent_list)
        x=1
        for i in ent_list:
            i=str(i.text)
            print(i)
            if i==entname:
                break
            else:
                x += 1
        print(x)
        zdyqqy_goal_ent_lingqu_button=zdyqqy_one_entmsg + '[%s]/div[2]/div[2]/a'%x
        self.web.find_element_by_xpath(zdyqqy_goal_ent_lingqu_button).click()#点击目标企业领取按钮
        yilingqu=self.web.find_element_by_xpath(zdyqqy_goal_ent_lingqu_button).text
        lingquchenggong_msg=self.web.find_element_by_xpath(xingchengliqiye_linquchenggong_msg).text
        #self.assertEqual(lingquchenggong_msg,'领取成功')#判断领取成功消息框是否出现
        #self.is_not_displayed(lingquchenggong_msg)#判断领取成功消息框是否消失
        self.web.find_element_by_xpath(wdkh_table).click()#判断目标企业是否在我的客户列表中
        wdkh_entname=self.web.find_element_by_xpath(wdkh_first_entname).text
        self.assertEqual(wdkh_entname,entname)
        print(wdkh_entname)

    def test_wlhk_lingqu(self):
        self.weilanhuoke_lingqu('')
if __name__ == "__main__":
    unittest.main()
