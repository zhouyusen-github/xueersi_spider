# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

'''
class XueersiPyTestPipeline(object):
    def process_item(self, item, spider):
        return item
'''
import pymysql

class MysqlPipeline(object):
    def __init__(self,host,user,password,database,port):
        self.host = "127.0.0.1"
        self.user = "root"
        self.password = "ZYSzys123#"
        self.database = "testAll1107" #每周数据换一次数据库名
        self.port = 3306

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            host = crawler.settings.get("MYSQL_HOST"),
            user = crawler.settings.get("MYSQL_USER"),
            password = crawler.settings.get("MYSQL_PASS"),
            database = crawler.settings.get("MYSQL_DATABASE"),
            port = crawler.settings.get("MYSQL_PORT"),
        )

    def open_spider(self, spider):
        '''负责连接数据库'''
        self.db = pymysql.connect(self.host,self.user,self.password,self.database,charset="utf8",port=self.port)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        '''执行数据表的写入操作'''
        #组装sql语句
        data = dict(item)
        keys = ','.join(data.keys())
        values=','.join(['%s']*len(data))
        sql = "insert into %s(%s) values(%s)"%(item.table,keys,values) #这就是正确sql插入格式，表名，字段名，值,也是正确的python字符串格式化
        #指定参数，并执行sql添加
        self.cursor.execute(sql,tuple(data.values()))
        #事务提交
        self.db.commit()
        return item

    def close_spider(self, spider):
        '''关闭连接数据库'''
        self.db.close()