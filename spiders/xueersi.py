# -*- coding: utf-8 -*-
import scrapy
import json

from xueersi_py_test.header_and_payload_build.gradeList_header_and_payload_build import gradeList_header
from xueersi_py_test.header_and_payload_build.classList_header_and_payload_build import header,payload2

from xueersi_py_test.cut_response_to_data.cut_response_to_data_all import cut_city,cut_city_detail,\
    cut_grade_list,cut_grade_list_detail,cut_courses_totalcount,cut_course_status,course_status_to_courseItem


class CitysSpider(scrapy.Spider):
    name = 'xueersi'
    allowed_domains = ['speiyou.com']#用于过滤url范围的
    #start_urls = ['http://speiyou.com/city/']#没有使用连接接口的方式

    def start_requests(self):
        url = "http://speiyou.com/city/"
        meta = {
            'control': 0
        }
        yield scrapy.Request(
            url=url,
            callback=self.parse_citys,
            meta=meta
        )

    def parse_citys(self, response):
        html_content = response.body.decode()
        citys = cut_city(html_content)
        for city in citys:
            item = cut_city_detail(city)
            #print(item)
            #yield item
            url = "https://www.speiyou.com/v2/pysite/grade/list"
            meta = {
                'control': 2,
                'areaCode': item['area'],#名字不同小心
                'cityName': item['name'],#尽管构建请求头用不到但是记录信息的时候要记录
                'pinyin': item['pinyin']#referer
            }
            headers = gradeList_header('')
            yield scrapy.Request(
                url=url,
                callback=self.parse_grades,
                method="GET",
                headers=headers,
                meta=meta,  # 传递信息给爬虫中间件来构造请求头
                dont_filter = True#关闭url去重，因为url不变的，我们是通过更改请求头获取新信息
            )

    def parse_grades(self, response):
        html_content = response.body.decode()
        grades = cut_grade_list(html_content)
        areaCode = response.meta['areaCode']
        cityName = response.meta['cityName']
        pinyin = response.meta['pinyin']
        for grade in grades:
            item = cut_grade_list_detail(grade,cityName,areaCode)
            #print(item)
            page = "1"
            gradeId = item['grd_id']
            payload = payload2(page, gradeId)

            headers = header('', '', '', '')
            url = "https://www.speiyou.com/v2/pysite/class/list"
            meta = {
                'control': 1,
                'areaCode': areaCode,
                'gradeId': gradeId,
                'Referer': 'https://www.speiyou.com/'+pinyin+'/list',#虽然这一条去掉，接口仍可以返回数据，但我加了
                'page': "1",
                'cityName': cityName,
                'grd_name': item["grd_name"]
            }
            yield scrapy.Request(
                url=url,
                callback=self.parse_courses_totalcount,
                method="POST",
                body=json.dumps(payload),
                headers=headers,
                meta=meta, # 传递信息给爬虫中间件来构造请求头
                dont_filter = True
            )

    #测试成功，并且可以确认是深度优先

    def parse_courses_totalcount(self, response):
        html_content = response.body.decode()
        areaCode = response.meta['areaCode']
        cityName = response.meta['cityName']
        gradeId = response.meta['gradeId']
        grd_name = response.meta['grd_name']
        item = cut_courses_totalcount(html_content, cityName, areaCode, gradeId, grd_name)

        if item["totalCount"] != 0:#有特殊情况会导致，即使有grade，也没有数据
            pages = item["totalCount"] // 10 + 1  # totalCount除10就是总页数
            for i in range(pages):
                page = str(i)
                payload = payload2(page, gradeId)
                print(page)
                headers = header('', '', '', '')
                url = "https://www.speiyou.com/v2/pysite/class/list"
                meta = {
                    'control': 1,
                    'areaCode': areaCode,
                    'gradeId': gradeId,
                    'Referer': 'https://www.speiyou.com/foshan/list',  # 这里后期要修改
                    'page': page,
                    'name': cityName,
                    'gradeName': grd_name
                }
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_courses_detail,
                    method="POST",
                    body=json.dumps(payload),
                    headers=headers,
                    meta=meta,  # 传递信息给爬虫中间件来构造请求头
                    dont_filter=True
                )

        pass


    def parse_courses_detail(self, response):
        string = response.body.decode()
        cityName = response.meta['name']
        cityCode = response.meta['areaCode']
        gradeName = response.meta['gradeName']
        gradeId = response.meta['gradeId']


        strings = cut_course_status(string)
        for i in strings:
            item = course_status_to_courseItem(i,cityName,cityCode,gradeName,gradeId)
            print(item)
        pass