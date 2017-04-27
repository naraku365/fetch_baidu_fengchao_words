#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import copy

import requests

from config import ini_config


UserAgent = ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, '
             'like Gecko) Chrome/32.0.1700.76 Safari/537.36')

HUMAN_HEADERS = {
    'Accept': ('text/html,application/xhtml+xml,application/xml;q=0.9,'
               'image/webp,*/*;q=0.8'),
    'User-Agent': UserAgent,
    'Accept-Encoding': 'gzip,deflate,sdch'
}


class Api(object):
    def __init__(self, cookie, user_id, token):
        self.headers = copy.deepcopy(HUMAN_HEADERS)
        self.headers.update({'Cookie': cookie})
        self.user_id = user_id
        self.token = token

    def get_result_words(self, keyword):
        params = '{"query":"%s","querytype":1,"regions":"0","device":0,"rgfilter":1,"entry":"kr_station","planid":"0","unitid":"0","needAutounit":false,"filterAccountWord":true,"attrShowReasonTag":[],"attrBusinessPointTag":[],"attrWordContainTag":[],"showWordContain":"","showWordNotContain":"","pageNo":1,"pageSize":1000,"orderBy":"","order":"","forceReload":false}'
        params %= keyword
        req_id = int(time.time() * 1000)
        post_data = {
            "path": "jupiter/GET/kr/word",
            "userid": self.user_id,
            "reqId": req_id,
            "params": params,
            "token": self.token,
        }
        url = ini_config.api_url.format(req_id=req_id)
        r = requests.post(url, headers=self.headers, data=post_data)
        data_dict = r.json()['data']
        result = []
        for item in data_dict['group'][0]['resultitem']:
            result.append(item)
        return result
