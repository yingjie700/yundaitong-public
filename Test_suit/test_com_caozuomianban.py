from selenium import webdriver
from config import config1
import unittest
import time
url=config1.get_login_msg.get_url()
cookie=config1.get_login_msg.get_cookie()
czmb_table = config1.get_login_msg.get_czmb_table()
caozuomianban_entname_list = config1.get_czmb_elm.get_weilanhuoke_all_entname()
wlhk_table=config1.get_login_msg.get_wlhk_table()
weilanhuoke_entname_list=config1.get_wlhk_elm.get_xinchengliqiye_all_entname()
class com_with_caozuomianban(unittest.TestCase):

    def setUp(self):
        self.web=webdriver.Chrome()
        self.web.get(url)
        self.web.add_cookie(cookie)
        self.web.get(url)
        self.web.implicitly_wait(10)
    def tearDown(self):
        self.web.quit()

    def com_weilanhuoke_entname(self):
        self.web.find_element_by_xpath(czmb_table).click()
        time.sleep(2)
        czmb_entlist =self.web.find_elements_by_xpath(caozuomianban_entname_list)
        czmb_entlist_list=[]
        for i in czmb_entlist:
            czmb_entlist_list.append(i.text)
        self.web.find_element_by_xpath(wlhk_table).click()
        wlhk_entlist=self.web.find_elements_by_xpath(weilanhuoke_entname_list)
        wlhk_entlist_list=[]
        for x in wlhk_entlist:
            wlhk_entlist_list.append(x.text)
        self.assertListEqual(czmb_entlist_list,wlhk_entlist_list)

    def test_com_weilanhuoke_entname(self):
        self.com_weilanhuoke_entname()

if __name__ == "__main__":
    unittest.main()
