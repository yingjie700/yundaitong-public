from selenium import webdriver
from config import config1
import unittest
import time
url=config1.get_login_msg.get_url()
cookie=config1.get_login_msg.get_cookie()
weilanhuoke_more=config1.get_czmb_elm.get_weilanhuoke_genduo_button()
wlhk_table=config1.get_login_msg.get_wlhk_table()
wlhk_xinchengliqiye_table=config1.get_wlhk_elm.get_xinchengliqiye_table()
czmb_table=config1.get_login_msg.get_czmb_table()
yinxiaoxiansuo_more=config1.get_czmb_elm.get_yinxiaoxiansuo_genduo_button()
yxxs_table=config1.get_login_msg.get_yxxs_table()
wodekehu_xianxialuru=config1.get_wdkh_elm.get_wdkh_xianxialuru()
wodekehu_more=config1.get_czmb_elm.get_wodekehu_genduo_button()
wodebaogao_more=config1.get_czmb_elm.get_wodebaogao_genduo_button()
wdbg_header_bgmc=config1.get_wdbg_elm.get_wdbg_header_bgmc()
wodekehu_xinzeng_button=config1.get_czmb_elm.get_wodekehu_xinzeng_button()
diyakuaidai_title=config1.get_xxkh_elm.get_diyakuaidai_title()
class Page_Jump(unittest.TestCase):
    def setUp(self):
        self.web=webdriver.Chrome()
        self.web.get(url)
        self.web.add_cookie(cookie)
        self.web.get(url)
        self.web.find_element_by_xpath(czmb_table).click()
        self.web.implicitly_wait(10)
    def tearDown(self):
        self.web.quit()

    def czmb_click_more(self):
        self.web.find_element_by_xpath(weilanhuoke_more).click()#围栏获客更多按钮
        wlhk_page=self.web.find_element_by_xpath(wlhk_xinchengliqiye_table).text
        self.assertEqual(wlhk_page,'新成立企业')
        self.web.find_element_by_xpath(czmb_table).click()#返回操作面板
        self.web.find_element_by_xpath(yinxiaoxiansuo_more).click()#营销线索更多按钮
        yxxs_lable_text=self.web.find_element_by_xpath(yxxs_table).text
        self.assertEqual(yxxs_lable_text,'营销线索')
        self.web.find_element_by_xpath(czmb_table).click()  # 返回操作面板
        self.web.find_element_by_xpath(wodekehu_more).click()#我的客户更多按钮
        wdkh_xxlr=self.web.find_element_by_xpath(wodekehu_xianxialuru).text
        self.assertEqual(wdkh_xxlr,'线下录入')
        self.web.find_element_by_xpath(czmb_table).click()  # 返回操作面板
        self.web.find_element_by_xpath(wodebaogao_more).click()#我的报告更多按钮
        wdbg_header_bgmc_assert=self.web.find_element_by_xpath(wdbg_header_bgmc).text
        self.assertEqual(wdbg_header_bgmc_assert,'报告名称')
        self.web.find_element_by_xpath(czmb_table).click()  # 返回操作面板
        self.web.find_element_by_xpath(wodekehu_xinzeng_button).click()#我的客户新增按钮
        diyakuaidai_title_assert=self.web.find_element_by_xpath(diyakuaidai_title).text
        self.assertEqual(diyakuaidai_title_assert,'抵押快贷')

    #def czmb_click_entname(self,entname):
    def test_page_jump(self):
        self.czmb_click_more()

if __name__ == "__main__":
    unittest.main()
