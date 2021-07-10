# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from xueersi_py_test.header_and_payload_build.classList_header_and_payload_build import header,payload2#给修改url和payload用的
from xueersi_py_test.header_and_payload_build.gradeList_header_and_payload_build import gradeList_header

import json


class XueersiPyTestSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class XueersiPyTestDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        #control是控制码，决定中间件是否做处理，和做何处理
        #control == 1 则修改请求头，payload，对应访问接口的请求
        #control == 0不做处理 ，对应某些普通request请求
        if request.meta['control'] == 1:
            areaCode = request.meta['areaCode']
            gradeId = request.meta['gradeId']
            Referer = request.meta['Referer']
            page = request.meta['page']
            # request.body = json.dumps(payload2(page,gradeId))
            #request.set_body(json.dumps(payload2(page, gradeId)))  # body要用这种方法才能修改,11/2日这个方法突然不行了，后来反正payload后来不用修改，索性直接在前面request生成，然后不修改
            # request.headers = header(areaCode, gradeId, Referer, page)#这样会报错要下面那种才行

            new_headers = header(areaCode, gradeId, Referer, page)
            print(request.headers)
            request.headers['areaCode'] = new_headers['areaCode']
            request.headers['nonce'] = new_headers['nonce']
            request.headers['sign'] = new_headers['sign']
            request.headers['timestamp'] = new_headers['timestamp']

            print(request.headers)

        if request.meta['control'] == 2:
            areaCode = request.meta['areaCode']
            new_headers = gradeList_header(areaCode)
            request.headers['areaCode'] = new_headers['areaCode']
            request.headers['nonce'] = new_headers['nonce']
            request.headers['sign'] = new_headers['sign']
            request.headers['timestamp'] = new_headers['timestamp']

            #一开始出错时缺了这三行
            #request.headers['accessid'] = new_headers['accessid']
            print(request.headers)





        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
