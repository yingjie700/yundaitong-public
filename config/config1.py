from configparser import ConfigParser
import json


class get_login_msg():#获取基本登陆信息
    def get_url(*self):
        global cp
        cp= ConfigParser()
        cp.read("D:\yundaitong\config\config.ini",encoding='UTF-8')
        url=cp.get('url','url')
        #print(url)
        return url

    def get_cookie(*self):
        cp = ConfigParser()
        cp.read("D:\yundaitong\config\config.ini",encoding='UTF-8')
        cookie =cp.get('cookie', 'cookie')
        #print(cookie)
        cookies=json.loads(cookie)
        return cookies
    def get_czmb_table(*self):
        czmb_table=cp.get('table','czmb_table')
        return czmb_table
    def get_yjss_table(*self):
        yjss_table=cp.get('table','yjss_table')
        return yjss_table
    def get_wlhk_table(*self):
        wlhk_table=cp.get('table','wlhk_table')
        return wlhk_table
    def get_yxxs_table(*self):
        yxxs_table=cp.get('table','yxxs_table')
        return yxxs_table
    def get_xxkh_table(*self):
        xxkh_table=cp.get('table','xxkh_table')
        return xxkh_table
    def get_wdkh_table(*self):
        wdkh_table=cp.get('table','wdkh_table')
        return wdkh_table
    def get_wdbg_table(*self):
        wdbg_table=cp.get('table','wdbg_table')
        return wdbg_table

class get_czmb_elm():#获取操作面板界面元素路径
    def get_weilanhuoke_one_entname(*self):
        weilanhuoke_one_entname=cp.get('caozuomianban_weilanhuoke','weilanhuoke_one_entname')
        return weilanhuoke_one_entname
    def get_weilanhuoke_all_entname(*self):
        weilanhuoke_all_entname=cp.get('caozuomianban_weilanhuoke','weilanhuoke_all_entname')
        return weilanhuoke_all_entname
    def get_weilanhuoke_linqu_button(*self):
        weilanhuoke_linqu_button=cp.get('caozuomianban_weilanhuoke','weilanhuoke_linqu_button')
        return weilanhuoke_linqu_button
    def get_weilanhuoke_genduo_button(*self):
        weilanhuoke_genduo_button=cp.get('caozuomianban_weilanhuoke','weilanhuoke_genduo_button')
        return weilanhuoke_genduo_button
    def get_yinxiaoxiansuo_genduo_button(*self):
        yinxiaoxiansuo_genduo_button=cp.get('caozuomianban_yinxiaoxiansuo','yinxiaoxiansuo_genduo_button')
        return yinxiaoxiansuo_genduo_button
    def get_wodekehu_genduo_button(*self):
        wodekehu_genduo_button=cp.get('caozuomianban_wodekehu','wodekehu_genduo_button')
        return wodekehu_genduo_button
    def get_wodebaogao_genduo_button(*self):
        wodebaogao_genduo_button=cp.get('caozuomianban_wodebaogao','wodebaogao_genduo_button')
        return wodebaogao_genduo_button
    def get_wodekehu_xinzeng_button(*self):
        wodekehu_xinzeng_button = cp.get('caozuomianban_wodekehu', 'wodekehu_xinzeng_button')
        return wodekehu_xinzeng_button

class get_wlhk_elm():
    def get_xingchengliqiye_one_entmsg(*self):
        xingchengliqiye_one_entmsg=cp.get('weilanhuoke_xinchengliqiye','xingchengliqiye_one_entmsg')
        return xingchengliqiye_one_entmsg
    def get_xinchengliqiye_one_entname(*self):
        xinchengliqiye_one_entname=cp.get('weilanhuoke_xinchengliqiye','xinchengliqiye_one_entname')
        return xinchengliqiye_one_entname
    def get_xinchengliqiye_all_entname(*self):
        xinchengliqiye_all_entname=cp.get('weilanhuoke_xinchengliqiye','xinchengliqiye_all_entname')
        return xinchengliqiye_all_entname
    def get_xinchengliqiye_table(*self):
        xinchengliqiye_table=cp.get('weilanhuoke_xinchengliqiye','xinchengliqiye_table')
        return xinchengliqiye_table
    def get_xingchengliqiye_linquchenggong_msg(*self):
        xingchengliqiye_linquchenggong_msg=cp.get('weilanhuoke_xinchengliqiye','xingchengliqiye_linquchenggong_msg')
        return xingchengliqiye_linquchenggong_msg

    def get_zdyqqy_table(*self):
        zdyqqy_table=cp.get('weilanhuoke_zhongdianyuanquqiye','table')
        return zdyqqy_table
    def get_zfyqqy_one_entmsg(*self):
        zfyqqy_one_entmsg=cp.get('weilanhuoke_zhongdianyuanquqiye','zfyqqy_one_entmsg')
        return zfyqqy_one_entmsg
    def get_zdyqqy_one_entname(*self):
        zdyqqy_one_entname=cp.get('weilanhuoke_zhongdianyuanquqiye','zdyqqy_one_entname')
        return zdyqqy_one_entname
    def get_zdyqqy_all_entname(*self):
        xinchengliqiye_all_entname=cp.get('weilanhuoke_zhongdianyuanquqiye','zdyqqy_all_entname')
        return xinchengliqiye_all_entname
    def get_zdyqqy_linquchenggong_msg(*self):
        xingchengliqiye_linquchenggong_msg=cp.get('weilanhuoke_zhongdianyuanquqiye','zdyqqy_linquchenggong_msg')
        return xingchengliqiye_linquchenggong_msg
class get_yxxs_elm():
    def get_kehulaiyuan_all(*self):
        kehulaiyuan_all=cp.get('yinxiaoxiansuo','kehulaiyuan_all')
        return kehulaiyuan_all
    def get_kehulaiyuan_zizhushengqin(*self):
        kehulaiyuan_zizhushengqin=cp.get('yinxiaoxiansuo','kehulaiyuan_zizhushengqin')
        return kehulaiyuan_zizhushengqin
    def get_kehulaiyuan_zhongjietuijian(*self):
        kehulaiyuan_zhongjietuijian=cp.get('yinxiaoxiansuo','kehulaiyuan_zhongjietuijian')
        return kehulaiyuan_zhongjietuijian
    def get_shengqinchanping_all(*self):
        shengqinchanping_all=cp.get('yinxiaoxiansuo','shengqinchanping_all')
        return shengqinchanping_all
    def get_shengqinchanping_diyakuaidai(*self):
        shengqinchanping_diyakuaidai=cp.get('yinxiaoxiansuo','shengqinchanping_diyakuaidai')
        return shengqinchanping_diyakuaidai
    def get_shengqinchanping_pingtaikuaidai(*self):
        shengqinchanping_pingtaikuaidai=cp.get('yinxiaoxiansuo','shengqinchanping_pingtaikuaidai')
        return shengqinchanping_pingtaikuaidai
    def get_shengqinchanping_xingyongkuaidai(*self):
        shengqinchanping_xingyongkuaidai=cp.get('yinxiaoxiansuo','shengqinchanping_xingyongkuaidai')
        return shengqinchanping_xingyongkuaidai
    def get_shengqinchanping_yunshuidai(*self):
        shengqinchanping_yunshuidai=cp.get('yinxiaoxiansuo','shengqinchanping_yunshuidai')
        return shengqinchanping_yunshuidai
    def get_shengqinchanping_qita(*self):
        shengqinchanping_qita=cp.get('yinxiaoxiansuo','shengqinchanping_qita')
        return shengqinchanping_qita
    def get_zhuangtai_all(*self):
        zhuangtai_all=cp.get('yinxiaoxiansuo','zhuangtai_all')
        return zhuangtai_all
    def get_zhaungtai_yilingqu(*self):
        zhaungtai_yilingqu=cp.get('yinxiaoxiansuo','zhaungtai_yilingqu')
        return zhaungtai_yilingqu
    def get_zhaungtai_weilingqu(*self):
        zhaungtai_weilingqu=cp.get('yinxiaoxiansuo','zhaungtai_weilingqu')
        return zhaungtai_weilingqu
    def get_ent_detail_msg(*self):
        ent_detail_msg=cp.get('yinxiaoxiansuo','ent_detail_msg')
        return ent_detail_msg
    def get_ent_detial_kehulaiyuan(*self):
        ent_detial_kehulaiyuan=cp.get('yinxiaoxiansuo','ent_detial_kehulaiyuan')
        return ent_detial_kehulaiyuan
    def get_ent_detial_zhuangtai(*self):
        ent_detial_zhuangtai=cp.get('yinxiaoxiansuo','ent_detial_zhuangtai')
        return ent_detial_zhuangtai
    def get_ent_detial_shengqingchanping(*self):
        ent_detial_shengqingchanping=cp.get('yinxiaoxiansuo','ent_detial_shengqingchanping')
        return ent_detial_shengqingchanping

class get_xxkh_elm():
    def get_diyakuaidai_title(*self):
        diyakuaidai_title=cp.get('xianxiakehu','diyakuaidai_title')
        return diyakuaidai_title
    def get_xingyongkuaidai_title(*self):
        xingyongkuaidai_title=cp.get('xianxiakehu','xingyongkuaidai_title')
        return xingyongkuaidai_title
    def get_pingtaikuaidai_title(*self):
        pingtaikuaidai_title=cp.get('xianxiakehu','pingtaikuaidai_title')
        return pingtaikuaidai_title
    def get_yunshuidai_title(*self):
        yunshuidai_title=cp.get('xianxiakehu','yunshuidai_title')
        return yunshuidai_title
    def get_xingyongkuaidai_apply_button(*self):
        xingyongkuaidai_apply_button=cp.get('xianxiakehu','xingyongkuaidai_apply_button')
        return xingyongkuaidai_apply_button
    def get_pingtaikuaidai_apply_button(*self):
        pingtaikuaidai_apply_button=cp.get('xianxiakehu','pingtaikuaidai_apply_button')
        return pingtaikuaidai_apply_button
    def get_yunshuidai_apply_button(*self):
        yunshuidai_apply_button=cp.get('xianxiakehu','yunshuidai_apply_button')
        return yunshuidai_apply_button
    def get_apply_page_title(*self):
        apply_page_title=cp.get('xianxiakehu','apply_page_title')
        return apply_page_title
    def get_other_qiyemingcheng_text(*self):
        other_qiyemingcheng_text=cp.get('xianxiakehu','other_qiyemingcheng_text')
        return other_qiyemingcheng_text
    def get_other_shijikongzhiren_text(*self):
        other_shijikongzhiren_text=cp.get('xianxiakehu','other_shijikongzhiren_text')
        return other_shijikongzhiren_text
    def get_other_shengfenzhenghao_text(*self):
        other_shengfenzhenghao_text=cp.get('xianxiakehu','other_shengfenzhenghao_text')
        return other_shengfenzhenghao_text
    def get_other_qiyedizhi_text(*self):
        other_qiyedizhi_text=cp.get('xianxiakehu','other_qiyedizhi_text')
        return other_qiyedizhi_text
    def get_submit_button(*self):
        submit_button=cp.get('xianxiakehu','submit_button')
        return submit_button
    def get_submit_sucess_msg(*self):
        submit_sucess_msg=cp.get('xianxiakehu','submit_sucess_msg')
        return submit_sucess_msg

class get_wdkh_elm():
    def get_wdkh_xianxialuru(*self):
        kehulaiyuan_xianxialuru=cp.get('wodekehu','kehulaiyuan_xianxialuru')
        return kehulaiyuan_xianxialuru
    def get_wdkh_first_entname(*self):
        first_entname=cp.get('wodekehu','first_entname')
        return first_entname

class get_wdbg_elm():
    def get_wdbg_header_bgmc(*self):
        kehulaiyuan_xianxialuru=cp.get('wodebaogao','header_bgmc')
        return kehulaiyuan_xianxialuru
