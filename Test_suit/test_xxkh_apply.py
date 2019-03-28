from selenium import webdriver
from config import config1
import unittest
import time
url=config1.get_login_msg.get_url()
cookie = config1.get_login_msg.get_cookie()
xxkh_table=config1.get_login_msg.get_xxkh_table()
apply_page_title=config1.get_xxkh_elm.get_apply_page_title()
other_qiyemingcheng_text=config1.get_xxkh_elm.get_other_qiyemingcheng_text()
other_shijikongzhiren_text=config1.get_xxkh_elm.get_other_shijikongzhiren_text()
other_shengfenzhenghao_text=config1.get_xxkh_elm.get_other_shengfenzhenghao_text()
other_qiyedizhi_text=config1.get_xxkh_elm.get_other_qiyedizhi_text()
submit_button=config1.get_xxkh_elm.get_submit_button()
submit_sucess_msg=config1.get_xxkh_elm.get_submit_sucess_msg()
wdkh_first_entname=config1.get_wdkh_elm.get_wdkh_first_entname()
class Xxkh_apply(unittest.TestCase):
    def setUp(self):
        self.web=webdriver.Chrome()
        self.web.get(url)
        self.web.add_cookie(cookie)
        self.web.get(url)
        self.web.implicitly_wait(10)
    def tearDown(self):
        self.web.quit()

    def apply_other_there_product(self,apply_product,entname,person_name,num,adress):
        self.web.find_element_by_xpath(xxkh_table).click()
        apply_button='//*[@id="risk-productList"]/div[1]/div[%s]/div[2]/button'%apply_product
        self.web.find_element_by_xpath(apply_button).click()
        self.web.find_element_by_xpath(other_qiyemingcheng_text).send_keys(entname)
        self.web.find_element_by_xpath(other_shijikongzhiren_text).send_keys(person_name)
        self.web.find_element_by_xpath(other_shengfenzhenghao_text).send_keys(num)
        self.web.find_element_by_xpath(other_qiyedizhi_text).send_keys(adress)
        self.web.find_element_by_xpath(submit_button).click()
        time.sleep(3)
        sucess_msg=self.web.find_element_by_xpath(submit_sucess_msg).text
        self.assertEqual(sucess_msg,'排查成功！')
        time.sleep(5)
        wdkh_entname=self.web.find_element_by_xpath(wdkh_first_entname).text
        self.assertEqual(wdkh_entname,entname)

    def test_apply_other_three_product(self):
        self.apply_other_there_product('2','小米科技有限责任公司','','33016587413543213545','asdasdasd')