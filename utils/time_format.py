#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from datetime import datetime, timedelta
import time


time_regex = re.compile(u'(\d+)(天前|小时前|分钟前)')
day_regex = re.compile(u'(\d+)月(\d+)日')


def get_time_from_ch(unicode_ch):
    now = datetime.now()
    result = time_regex.findall(unicode_ch)
    if not result:
        result = day_regex.findall(unicode_ch)
        if not result:
            return None
        else:
            return '%s-%s-%s 00:00:00' % (now.year, result[0][0], result[0][1])
    num, time_ch = result[0]
    num = int(num)
    target_date_time = None
    if time_ch == u'天前':
        target_date_time = now - timedelta(days=num)
    elif time_ch == u'小时前':
        target_date_time = now - timedelta(hours=num)
    elif time_ch == u'分钟前':
        target_date_time = now - timedelta(minutes=num)
    if target_date_time:
        target_date_time = target_date_time.strftime('%Y-%m-%d %H:%M:%S')
    return target_date_time


def str_time_to_datetime(str_time, format_str='%Y-%m-%d %H:%M:%S'):
    return datetime.strptime(str_time, format_str)


def get_now_str():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_now():
    return datetime.now()


def get_today_str():
    return datetime.now().strftime('%Y-%m-%d')


def get_today_hour_str():
    return datetime.now().strftime('%Y-%m-%d %H')


def get_today_year():
    return datetime.now().strftime('%Y')


def get_timestamp(date_time=None):
    if not date_time:
        date_time = datetime.now()
    return int(time.mktime(date_time.timetuple()))


def get_year_month_day(target_date_str='', now=False):
    if now:
        now = datetime.now()
        return [now.year, now.month, now.day]
    else:
        year_month_day = target_date_str.split(" ")[0].split("-")
        return [int(s) for s in year_month_day]


def is_expire(target_date_str, effective_days=1):
    if not target_date_str:
        return True

    year_month_day = get_year_month_day(target_date_str)
    target_datetime = datetime(*year_month_day)

    now = datetime.now()
    today_datetime = datetime(now.year, now.month, now.day)

    return target_datetime + timedelta(days=effective_days) < today_datetime


def is_today(target_date_str):
    return get_year_month_day(target_date_str) == get_year_month_day(now=True)


def get_date_time_from_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp)


def get_day_str_from_timestamp(timestamp):
    d = get_date_time_from_timestamp(timestamp)
    return datetime_to_str_time(d, format_str='%Y-%m-%d')


def datetime_to_str_time(date, format_str='%Y-%m-%d %H:%M:%S'):
    return date.strftime(format_str)


def str_time_to_str_day_by_format(date_str, format_str='%Y-%m-%d %H:%M:%S'):
    d = datetime.strptime(date_str, format_str)
    return datetime_to_str_time(d, format_str='%Y-%m-%d')


def to_tomorrow_second():
    return 86400 - (int(time.time()) - time.timezone) % 86400


def get_last_day_str(last_day=1):
    last_day_datetime = get_now() - timedelta(days=last_day)
    return last_day_datetime.strftime('%Y-%m-%d')


if __name__ == '__main__':
    print get_time_from_ch(u'9分钟前')
    print get_time_from_ch(u'9小时前')
    print get_time_from_ch(u'9天前')
    print get_last_day_str(3)
