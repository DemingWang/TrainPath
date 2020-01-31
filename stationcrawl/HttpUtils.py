# -*- encoding: utf-8 -*-

"""
 Http 网络请求工具
 
 Author: zsyoung
 
 Date: 2019/01/09 15:00
"""

import requests
import random
from retrying import retry
from stationcrawl import LogUtils
from stationcrawl.Constants import *
from stationcrawl.ArgList import get_key


@retry(wait_fixed=3000, stop_max_attempt_number=9)
def get_html(url):
    """
    获取Html源码

    :param url: 链接地址
    :return: html源码
    """
    try:
        response = requests.get(url, headers=__gen_headers())
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
        else:
            print("网络访问出错，非200")
            print(response.status_code)
    except:
        LogUtils.log('./error.log', url)
        raise Exception('网络异常')


@retry(wait_fixed=3000, stop_max_attempt_number=9)
def get_bytes(url,arg):
    """
    获取File字节流

    :param url: File地址
    :return: response.content
    """
    init_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
    from_station_name = get_key(STATION_DICT, arg[1])
    to_station_name = get_key(STATION_DICT, arg[2])
    post_data= {'back_train_date':str(arg[0]),
                '_json_att':"",'flag':'dc',
                'leftTicketDTO.from_station':str(arg[1]),
                'leftTicketDTO.to_station':str(arg[2]),
                # 'leftTicketDTO.from_station_name':str(arg[1]),
                # 'leftTicketDTO.to_station_name':str(arg[2]),
                'leftTicketDTO.train_date':str(arg[0]),
                'pre_step_flag':'index',
                'purpose_code':'ADULT'}
 
    init_resp=requests.post(init_url,data=post_data,allow_redirects=True,verify=False)
    cookies=init_resp.cookies
    # cookies.set('_jc_save_fromStation', str(arg[1]) +','+str(arg[1]), domain='kyfw.12306.cn', path='/')
    # cookies.set('_jc_save_toStation', str(arg[2])+','+str(arg[2]), domain='kyfw.12306.cn', path='/')
    cookies.set('_jc_save_fromStation', str(arg[1]), domain='kyfw.12306.cn', path='/')
    cookies.set('_jc_save_toStation', str(arg[2]), domain='kyfw.12306.cn', path='/')
    cookies.set('_jc_save_fromDate', str(arg[0]), domain='kyfw.12306.cn', path='/')
    cookies.set('_jc_save_toDate', str(arg[0]), domain='kyfw.12306.cn', path='/')
    cookies.set('_jc_save_wfdc_flag', 'dc', domain='kyfw.12306.cn', path='/')
    try:
        response = requests.get(url,cookies=cookies,headers=__gen_headers(),verify=False)#, headers=__gen_headers()
        if response.status_code == 200:
            return response.content.decode('utf-8')
        else:
            print("网络访问出错，非200")
            print(response.status_code)
    except:
        LogUtils.log('./error.log', url)
        raise Exception('网络异常')


def __gen_headers():
    headers = {
        "User-Agent": USER_AGENTS[random.randint(0, len(USER_AGENTS) - 1)],
        # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    return headers
