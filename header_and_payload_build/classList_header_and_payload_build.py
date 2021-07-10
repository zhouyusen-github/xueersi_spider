# -*- coding: utf-8 -*-
import time
import hmac
import random
#!!!本文件用于写构建headers和payload的函数


'''
重要变量解释
areacode：城市代码
gradeId:年级（一年级为1，小班为-8）
page：第几页
limit：一页显示条目数，所有网页都是10条，我也不知道设1000会怎么样
'''
'''
header和payload共用默认变量，记得要改一起改
mode
limit
'''
#payload
def payload2(page,gradeId):
    return payload(page,gradeId)

def payload(page,gradeId):
    mode = "1"
    word = ""
    limit = "10"
    payload = payload_root(limit,mode,page,word,gradeId)
    return payload
#header
#headers中有很多可以注释，仍能正常返回数据，但是我决定还是保留这些,使我的访问尽可能看起来正常
def header(areaCode,gradeId,Referer,#城市，年级会有很多页
           page):#具体哪一页
    # 以后再调
    Cookie = 'XesAnalyticsGid=A9C52236-9958-4F97-A9EE-FCFD6E443009; aliyungf_tc=AQAAAJA4938eMw0AEN1eL0IMf7jN9D41'
    User_Agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Mobile Safari/537.36'


    #默认项
    Accept = 'application/json, text/plain, */*'
    Accept_Encoding = 'gzip, deflate, br'
    Accept_Language = 'zh-CN,zh;q=0.9,en;q=0.8'
    accessid = 'e90fb0f90e8949f6ac073e624b30ae23'  #一个多月了不同住址都没变过
    algorithm = 'HmacSHA1'
    client_type = '4'
    Connection = 'keep-alive'
    #Content_Length = '58'
    Content_Type = 'application/json;charset=UTF-8'
    Host = 'www.speiyou.com'
    Origin = 'https://www.speiyou.com'
    Sec_Fetch_Mode = 'cors'
    Sec_Fetch_Site = 'same-origin'

    limit = "10"
    mode = "1"
    HmacSHA1_Key = "39f128dd752c4ddbb29a61cfd2bde827"#要在js代码中才能找到



    header = header_root(Accept,Accept_Encoding,Accept_Language,accessid,algorithm,areaCode,client_type,Connection,
                Content_Type,Cookie,Host,Origin,Referer,Sec_Fetch_Mode,Sec_Fetch_Site,User_Agent,
                gradeId,limit,mode,nonce,page,HmacSHA1_Key)
    return header


#分开两个函数，是为了以后大量爬取时，可以调整更多避免反爬
def header_root(Accept,Accept_Encoding,Accept_Language,accessid,algorithm,areaCode,client_type,Connection,
                Content_Type,Cookie,Host,Origin,Referer,Sec_Fetch_Mode,Sec_Fetch_Site,User_Agent,
                gradeId,limit,mode,nonce,page,HmacSHA1_Key):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'accessid': 'e90fb0f90e8949f6ac073e624b30ae23',
        'algorithm': 'HmacSHA1',
        'areaCode': '0757',
        'client_type': '4',
        'Connection': 'keep-alive',
        #'Content-Length': '58',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': 'XesAnalyticsGid=A9C52236-9958-4F97-A9EE-FCFD6E443009; aliyungf_tc=AQAAAJA4938eMw0AEN1eL0IMf7jN9D41',
        'Host': 'www.speiyou.com',
        'nonce': '157042340323352cb2ece263c4f298bd9ff37a308af07',
        'Origin': 'https://www.speiyou.com',
        'Referer': 'https://www.speiyou.com/foshan/list',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'sign': '5833BE4771172F4D5EAC814E0CDA3498C8F41942',
        'timestamp': '1570423403233',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Mobile Safari/537.36'
    }
    headers['Accept'] = Accept
    headers['Accept-Encoding'] = Accept_Encoding
    headers['Accept-Language'] = Accept_Language
    headers['accessid'] = accessid
    headers['algorithm'] = algorithm
    headers['areaCode'] = areaCode
    headers['client_type'] = client_type
    headers['Connection'] = Connection
    #headers['Content-Length'] = Content_Length
    headers['Content-Type'] = Content_Type
    headers['Cookie'] = Cookie
    headers['Host'] = Host
    headers['Origin'] = Origin
    headers['Referer'] = Referer
    headers['Sec-Fetch-Mode'] = Sec_Fetch_Mode
    headers['Sec-Fetch-Site'] = Sec_Fetch_Site
    headers['User-Agent'] = User_Agent

    headers['timestamp'] = timestamp()
    headers['nonce'] = nonce(headers['timestamp'])
    headers['sign'] = sign(accessid,algorithm,client_type,gradeId,limit,mode,headers['nonce'],page,headers['timestamp'],HmacSHA1_Key)
    return headers

#两个headers都有这一块
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

def sign(accessid,algorithm,client_type,gradeId,limit,mode,nonce,page,timestamp,HmacSHA1_Key):
    # 例子：accessid=e90fb0f90e8949f6ac073e624b30ae23&algorithm=HmacSHA1&client_type=4&gradeId=3&limit=10&mode=1&nonce=15709423197300000000000004000b000000000000000&page=5&timestamp=1570942319730
    content = "accessid=" + accessid + "&algorithm=" + algorithm + "&client_type=" + client_type + "&gradeId=" + gradeId + "&limit=" + limit + "&mode=" + mode + "&nonce=" + nonce + "&page=" + str(
    page) + "&timestamp=" + timestamp
    sign = str(hash_hmac(HmacSHA1_Key, content))
    return sign

#HMACSHA1 加密模块
from hashlib import sha1
def hash_hmac(key, code):
    hmac_code = hmac.new(key.encode(), code.encode(), sha1)
    return hmac_code.hexdigest()




def payload_root(limit,mode,page,word,gradeId):
    payload = {}

    payload['limit'] = limit
    payload['mode'] = mode
    payload['page'] = page
    payload['word'] = word
    payload['gradeId'] = gradeId
    return payload

