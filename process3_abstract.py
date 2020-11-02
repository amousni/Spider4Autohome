# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 13:52:23 2020

@author: al
"""
'''
with open('all.txt', 'r', encoding='utf-8') as f:
    data_str = f.read()

data_list = data_str.split('\n')
print(data_list[:10])
'''

# coding=utf-8

import sys
import json
import base64
import time


# make it work in both python2 both python3
IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode

# skip https auth
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = 'kuqB6YVGSywzioG6zrtWlAWY'

SECRET_KEY = 'eZqGVd304QorahDGZtrXAbxL3Da5Vzg4'

COMMENT_TAG_URL = "https://aip.baidubce.com/rpc/2.0/nlp/v2/comment_tag"

"""  TOKEN start """
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'


"""
    get token
"""
def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)
    if (IS_PY3):
        result_str = result_str.decode()


    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print ('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print ('please overwrite the correct API_KEY and SECRET_KEY')
        exit()

"""
    call remote http server
"""
def make_request(url, comment):
    print("---------------------------------------------------")
    print(comment)
    print('')

    response = request(url, json.dumps(
    {
        "text": comment,
        # 13为3C手机类型评论，其他类别评论请参考 https://ai.baidu.com/docs#/NLP-Apply-API/09fc895f
        "type": 10
    }))

    data = json.loads(response)

    if "error_code" not in data or data["error_code"] == 0:
        for item in data["items"]:
            print(item['abstract'])
    else:
        # print error response
        print(response)

    # 防止qps超限
    time.sleep(0.5)

"""
    call remote http server
"""
def request(url, data):
    req = Request(url, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()
        if (IS_PY3):
            result_str = result_str.decode()
        return result_str
    except  URLError as err:
        print(err)

if __name__ == '__main__':

    comment1 = "对于电车来说第二大亮点就是动力，电车上来就是最大功率，比燃油车加速要快很多。我有的时候上来就深踩油门，胎有点打滑，估计是ESP介入后才不打滑，推背感很强。"
    comment2 = "我想是增加了电池，车身加重的缘故，后悬架改成独立悬架，车身很稳，过一般路段舒适性不错，噪音控制的也很好，座椅软硬适中。分区空调"
    comment3 = "性价比还是不错的，除了电量稍微差点，其他的都是不错的，其实我感觉电量还是有提升空间的，因为后备箱下面放的是备胎，如果改成电池组，续航里程提升一倍应该没什么问题。还是那句老话，买了就是对的，不喜欢，感觉性价比不好的，就不会买，买了就是我认为最好的"

    # get access token
    token = fetch_token()

    # concat url
    url = COMMENT_TAG_URL + "?charset=UTF-8&access_token=" + token

    make_request(url, comment1)
    make_request(url, comment2)
    make_request(url, comment3)
