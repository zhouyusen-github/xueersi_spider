#没有payload
'''
Accept: application/json, text/plain, */*
accessid: e90fb0f90e8949f6ac073e624b30ae23
algorithm: HmacSHA1
areaCode: 1111
client_type: 4
nonce: 157234440890022037cb63e8544b3a4078928bead55cc
Referer: https://www.speiyou.com/city
Sec-Fetch-Mode: cors
sign: 4CA4C638077E765C8B2E7D420E41945670D1AF96
timestamp: 1572344408900
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36
'''


import time
import hmac
import random

def gradeList_header(areaCode):
    headers = {
        # 'Accept': 'application/json, text/plain, */*',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
         'accessid': 'e90fb0f90e8949f6ac073e624b30ae23',
         'algorithm': 'HmacSHA1',
        'areaCode': '1111',
         'client_type': '4',
        # 'Connection': 'keep-alive',
        # 'Content-Length': '58',
        'Content-Type': 'application/json;charset=UTF-8',

        # 'Cookie': 'XesAnalyticsGid=A9C52236-9958-4F97-A9EE-FCFD6E443009; aliyungf_tc=AQAAAJA4938eMw0AEN1eL0IMf7jN9D41',
        # 'Host': 'www.speiyou.com',
        'nonce': '157042340323352cb2ece263c4f298bd9ff37a308af07',
        # 'Origin': 'https://www.speiyou.com',
        # 'Referer': 'https://www.speiyou.com/foshan/list',
        # 'Sec-Fetch-Mode': 'cors',
        # 'Sec-Fetch-Site': 'same-origin',
        'sign': '5833BE4771172F4D5EAC814E0CDA3498C8F41942',
        'timestamp': '1570423403233',
        # 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Mobile Safari/537.36'
    }
    t = time.time()
    mst = int(round(t * 1000))
    timestamp = str(mst)

    # 时间戳
    headers['timestamp'] = timestamp
    #print(headers['timestamp'])
    # 密钥内容的一部分
    nonce = timestamp + "52cb2ece263c4f298bd9ff37a308af07"
    headers['nonce'] = nonce
    #print(headers['nonce'])

    # 密钥内容合成
    # 例子：accessid=e90fb0f90e8949f6ac073e624b30ae23&algorithm=HmacSHA1&client_type=4&gradeId=3&limit=10&mode=1&nonce=15709423197300000000000004000b000000000000000&page=5&timestamp=1570942319730

    # 网页代码中固定值content，也是HmacSHA1加密的内容
    accessid = "e90fb0f90e8949f6ac073e624b30ae23"
    headers['accessid'] = accessid
    algorithm = "HmacSHA1"
    headers['algorithm'] = algorithm
    client_type = "4"
    headers['client_type'] = client_type

    content = "accessid=" + accessid + "&algorithm=" + algorithm + "&client_type=" + client_type + "&nonce=" + nonce + "&timestamp=" + timestamp
    # HmacSHA1加密的key
    key = "39f128dd752c4ddbb29a61cfd2bde827"  # 要在js代码中才能找到

    # hmacSHA1加密结果
    sign = str(hash_hmac(key, content))
    headers['sign'] = sign

    #print("gradeList_header_and_payload_build")

    return headers


'''
def gradeList_header(areaCode):
    accessid = "e90fb0f90e8949f6ac073e624b30ae23"
    algorithm = "HmacSHA1"
    client_type = "4"
    Content_Type = 'application/json;charset=UTF-8'
    HmacSHA1_Key = "39f128dd752c4ddbb29a61cfd2bde827"
    header = gradeList_header_root(accessid, algorithm, areaCode, client_type,
                Content_Type, HmacSHA1_Key)

    return header
'''

#分开两个函数，是为了以后大量爬取时，可以调整更多避免反爬
def gradeList_header_root(accessid,algorithm,areaCode,client_type,
                Content_Type,HmacSHA1_Key):
    headers = {
        #'accessid': 'e90fb0f90e8949f6ac073e624b30ae23',
        #'client_type': '4',
        'areaCode': '0757',
        'Content-Type': 'application/json;charset=UTF-8',
        'nonce': '157042340323352cb2ece263c4f298bd9ff37a308af07',
        'sign': '5833BE4771172F4D5EAC814E0CDA3498C8F41942',
        'timestamp': '1570423403233',


    }

    headers['areaCode'] = areaCode
    headers['Content-Type'] = Content_Type
    headers['timestamp'] = timestamp()
    headers['nonce'] = nonce(headers['timestamp'])
    headers['sign'] = sign(accessid,algorithm,client_type,headers['nonce'],headers['timestamp'],HmacSHA1_Key)

    return headers


def nonceRandomPart():
    numbers1 = "0123456789abcdef"
    list = []
    for i in range(32):
        random1 = random.randint(0, 15)
        a = numbers1[random1]
        list.append(a)
    list[12]='4'
    numbers2="89ab"
    random2 = random.randint(0, 3)
    list[16] = numbers2[random2]
    answer = ''.join(list)  # pyhon也有join还是列表join好一点
    return answer

def nonce(timestamp):
    nonce = timestamp + nonceRandomPart()
    return nonce

def timestamp():
    t = time.time()
    mst = int(round(t * 1000))
    timestamp = str(mst)
    return timestamp

def sign(accessid,algorithm,client_type,nonce,timestamp,HmacSHA1_Key):
    content = "accessid=" + accessid + "&algorithm=" + algorithm + "&client_type=" + client_type + "&nonce=" + nonce + "&timestamp=" + timestamp
    sign = str(hash_hmac(HmacSHA1_Key, content))
    return sign

#HMACSHA1 加密模块
from hashlib import sha1
def hash_hmac(key, code):
    hmac_code = hmac.new(key.encode(), code.encode(), sha1)
    return hmac_code.hexdigest()