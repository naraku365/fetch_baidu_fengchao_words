#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback
import time
import json

from selenium import webdriver

from config import ini_config
from utils.log import logger
from utils.misc import to_unicode


class BaiduBrowser(object):
    def __init__(self, cookie_json=''):
        if not ini_config.browser_driver:
            browser_driver_name = 'Firefox'
        else:
            browser_driver_name = ini_config.browser_driver
        browser_driver_class = getattr(webdriver, browser_driver_name)

        if ini_config.browser_driver == 'Chrome':
            self.browser = browser_driver_class(executable_path=ini_config.executable_path)
        else:
            self.browser = browser_driver_class()

        # 设置超时时间
        self.browser.set_page_load_timeout(50)
        # 设置脚本运行超时时间
        self.browser.set_script_timeout(10)
        # 百度用户名
        self.user_name = to_unicode(ini_config.user_name)
        # 百度密码
        self.password = ini_config.password
        self.cookie_json = cookie_json

    def __del__(self):
        self.close()

    def is_login(self):
        # 如果初始化BaiduBrowser时传递了cookie信息，则检测一下是否登录状态
        self.login_with_cookie(self.cookie_json)
        # 访问待检测的页面
        self.browser.get(ini_config.user_center_url)
        html = self.browser.page_source
        print html
        # 检测是否有登录成功标记
        return to_unicode(ini_config.login_sign) in to_unicode(html)

    def init_login(self, check_login=True):
        # 判断是否需要登录
        need_login = False
        if not self.cookie_json:
            logger.info(u'因无历史cookie，本次执行需要登录百度')
            need_login = True
        elif check_login and not self.is_login():
            logger.info(u'加载历史cookie登录失败，本次执行需要登录百度')
            need_login = True
        else:
            logger.info(u'本次执行无需登录百度')
        # 执行浏览器自动填表登录，登录后获取cookie
        if need_login:
            self.login(self.user_name, self.password)
            self.cookie_json = self.get_cookie_json()

    def get_env_info(self):
        url = ini_config.search_url
        env_info = {}
        while 1:
            try:
                self.browser.get(url)
                time.sleep(3)
                # 获取要用到的token和user_id的值
                token = self.browser.execute_script(
                    'return nirvana.env.TOKEN;'
                )
                user_id = self.browser.execute_script(
                    'return nirvana.env.USER_ID;'
                )
                if token and user_id:
                    env_info['token'] = token
                    env_info['user_id'] = user_id
                    logger.info(env_info)
                    break
            except:
                logger.error(traceback.format_exc())
        return env_info

    def login(self, user_name, password):
        login_url = ini_config.login_url
        # 访问登陆页
        self.browser.get(login_url)
        time.sleep(2)

        # 自动填写表单并提交，如果出现验证码需要手动填写
        while 1:
            try:
                user_name_obj = self.browser.find_element_by_id(
                    'uc-common-account'
                )
                break
            except:
                logger.error(traceback.format_exc())
                time.sleep(1)
        user_name_obj.send_keys(user_name)
        ps_obj = self.browser.find_element_by_id('ucsl-password-edit')
        ps_obj.send_keys(password)
        sub_obj = self.browser.find_element_by_id('submit-form')
        sub_obj.click()
        # 如果页面的url没有改变，则继续等待
        while 1:
            if ini_config.success_url_sign in self.browser.current_url:
                break
            time.sleep(1)

    def close(self):
        if getattr(self, 'browser'):
            if self.browser:
                try:
                    self.browser.quit()
                except:
                    pass

    def get_cookie_json(self):
        return json.dumps(self.browser.get_cookies())

    def get_cookie_str(self, cookie_json=''):
        if cookie_json:
            cookies = json.loads(cookie_json)
        else:
            cookies = self.browser.get_cookies()
        return '; '.join(['%s=%s' % (item['name'], item['value'])
                          for item in cookies])

    def login_with_cookie(self, cookie_json):
        self.browser.get('https://www.baidu.com/')
        for item in json.loads(cookie_json):
            try:
                self.browser.add_cookie(item)
            except:
                continue
