from selenium import webdriver
from config import config1
import unittest
import time
url=config1.get_login_msg.get_url()
cookie = config1.get_login_msg.get_cookie()
yxxs_table=config1.get_login_msg.get_yxxs_table()
kehulaiyuan_all=config1.get_yxxs_elm.get_kehulaiyuan_all()
kehulaiyuan_zizhushengqin=config1.get_yxxs_elm.get_kehulaiyuan_zizhushengqin()
kehulaiyuan_zhongjietuijian=config1.get_yxxs_elm.get_kehulaiyuan_zhongjietuijian()
shengqinchanping_all=config1.get_yxxs_elm.get_shengqinchanping_all()
shengqinchanping_diyakuaidai=config1.get_yxxs_elm.get_shengqinchanping_diyakuaidai()
shengqinchanping_pingtaikuaidai=config1.get_yxxs_elm.get_shengqinchanping_pingtaikuaidai()
shengqinchanping_xingyongkuaidai=config1.get_yxxs_elm.get_shengqinchanping_xingyongkuaidai()
shengqinchanping_yunshuidai=config1.get_yxxs_elm.get_shengqinchanping_yunshuidai()
shengqinchanping_qita=config1.get_yxxs_elm.get_shengqinchanping_qita()
zhuangtai_all=config1.get_yxxs_elm.get_zhuangtai_all()
zhuangtai_yilingqu=config1.get_yxxs_elm.get_zhaungtai_yilingqu()
zhuangtai_weilingqu=config1.get_yxxs_elm.get_zhaungtai_weilingqu()
ent_detail_msg=config1.get_yxxs_elm.get_ent_detail_msg()
ent_detial_kehulaiyuan=config1.get_yxxs_elm.get_ent_detial_kehulaiyuan()
ent_detial_zhuangtai=config1.get_yxxs_elm.get_ent_detial_zhuangtai()
ent_detial_shengqingchanping=config1.get_yxxs_elm.get_ent_detial_shengqingchanping()
class Weilanhuoke_lingqu(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.web=webdriver.Chrome()
        self.web.get(url)
        self.web.add_cookie(cookie)
        self.web.get(url)
        self.web.implicitly_wait(10)

    @classmethod
    def tearDownClass(self):
        self.web.quit()

    def yxxs_shaixuan(self,tiaojian,tiaojian_msg):
        self.web.find_element_by_xpath(yxxs_table).click()
        self.web.find_element_by_xpath(tiaojian).click()#条件筛选按钮
        tiaojian_name=self.web.find_element_by_xpath(tiaojian).text#所点击条件的text文字，用于断言
        print(tiaojian_name)
        try:
            self.web.find_elements_by_xpath(tiaojian_msg)
            try:
                tiaojian_msg_text=self.web.find_elements_by_xpath(tiaojian_msg)#获取列表中筛选后的条件集合
                time.sleep(2)

                if tiaojian_msg == ent_detial_shengqingchanping:
                    for tj in tiaojian_msg_text:  # 循环断言集合中的每个元素
                        print(tj.text)
                        tiaojian_name_all='贷款产品：'+tiaojian_name
                        self.assertEqual(tj.text, tiaojian_name_all)
                elif tiaojian == zhuangtai_weilingqu:
                    for tj in tiaojian_msg_text:  # 循环断言集合中的每个元素
                        print(tj.text)
                        tj_all='未'+tj.text
                        print(tj_all)
                        self.assertEqual(tj_all, tiaojian_name)
                else:
                    print('执行2')
                    for tj in tiaojian_msg_text:  # 循环断言集合中的每个元素
                        print(tj.text)
                        self.assertEqual(tj.text,tiaojian_name)
            except:
                raise
        except:
            try:
                self.web.find_element_by_xpath('//*[@id="marketingCluesList"]/p')
                print('no data')
            except:
                raise
        self.web.refresh()
        '''
    def test_yxxs_shaixuan1(self):
        self.yxxs_shaixuan(kehulaiyuan_zizhushengqin,ent_detial_kehulaiyuan)
    def test_yxxs_shaixuan2(self):
        self.yxxs_shaixuan(kehulaiyuan_zhongjietuijian,ent_detial_kehulaiyuan)
        '''
    def test_yxxs_shaixuan3(self):
        self.yxxs_shaixuan(zhuangtai_weilingqu,ent_detial_zhuangtai)
    def test_yxxs_shaixuan4(self):
        self.yxxs_shaixuan(zhuangtai_yilingqu,ent_detial_zhuangtai)
    def test_yxxs_shaixuan5(self):
        self.yxxs_shaixuan(shengqinchanping_xingyongkuaidai,ent_detial_shengqingchanping)
    def test_yxxs_shaixuan6(self):
        self.yxxs_shaixuan(shengqinchanping_yunshuidai,ent_detial_shengqingchanping)
    def test_yxxs_shaixuan7(self):
        self.yxxs_shaixuan(shengqinchanping_diyakuaidai,ent_detial_shengqingchanping)


if __name__ == "__main__":
    unittest.main()














