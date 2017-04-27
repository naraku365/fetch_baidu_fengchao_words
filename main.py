#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import traceback

import chardet

from browser import BaiduBrowser
from utils.log import logger
from config import ini_config
from api import Api
from utils.misc import utf8

if os.name in ['nt']:
    FILE_NAME_ENCODING = 'gbk'
else:
    FILE_NAME_ENCODING = 'utf-8'


def main():
    logger.info(u'请确保你填写的账号密码能够成功登陆百度')
    # 创建data目录
    result_folder = ini_config.out_file_path
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    s = BaiduBrowser()
    s.init_login()
    logger.info(u'登陆成功')
    cookie_str = s.get_cookie_str()
    env_info = s.get_env_info()
    s.close()
    api = Api(cookie_str, env_info['user_id'], env_info['token'])

    fp = open(ini_config.keywords_task_file_path, 'rb')
    task_list = fp.readlines()
    fp.close()

    root = os.path.dirname(os.path.realpath(__file__))
    for keyword in task_list:
        try:
            keyword = keyword.strip()
            if not keyword:
                continue
            detect_result = chardet.detect(keyword)
            encoding = detect_result['encoding'] if detect_result else 'gbk'
            keyword_unicode = keyword.decode(encoding, 'ignore')
            keyword = keyword_unicode.encode('utf-8', 'ignore')
            file_name = ini_config.result_file_path.format(keyword_unicode.encode(FILE_NAME_ENCODING))
            result_file_path = os.path.join(root, file_name)
            logger.info('%s start' % keyword_unicode)
            result = api.get_result_words(keyword)
            save_words(result_file_path, result)
            time.sleep(1)
        except:
            print traceback.format_exc()


def save_words(file_path, data_list, only_words_pv=True):
    with open(file_path, 'w') as f:
        for result in data_list:
            if only_words_pv:
                line = 'word:{}\tpv:{}\r\n'.format(utf8(result['word']), result['pv'])
            else:
                line = '{}\r\n'.format(str(result))
            f.write(line)


if __name__ == '__main__':
    main()
