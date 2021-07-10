# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XueersiPyTestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

#城市
class CityItem(scrapy.Item):
    table = "citys" #表名别忘了加
    id = scrapy.Field()
    name = scrapy.Field()
    area = scrapy.Field()
    pinyin = scrapy.Field()
    local_city = scrapy.Field()
    snapshot_time = scrapy.Field()

class gradeItem(scrapy.Item):
    table = "grades"
    grd_id = scrapy.Field()
    grd_name = scrapy.Field()
    cla_gt_id = scrapy.Field()
    cla_gt_name = scrapy.Field()

    #用于后期分析
    name = scrapy.Field()
    areaCode = scrapy.Field()

    snapshot_time = scrapy.Field()

class coursesTotalCountItem(scrapy.Item):
    table = "courses_totalCount"

    name = scrapy.Field()
    areaCode = scrapy.Field()
    grd_id = scrapy.Field()
    grd_name = scrapy.Field()

    status = scrapy.Field()
    code = scrapy.Field()
    msg = scrapy.Field()
    totalCount = scrapy.Field()


    snapshot_time = scrapy.Field()



#课程详细信息
class courseItem(scrapy.Item):
    table = "courses_test1"

    cityName = scrapy.Field()
    cityCode = scrapy.Field()
    gradeName = scrapy.Field()
    gradeId = scrapy.Field()

    class_id = scrapy.Field()
    class_name = scrapy.Field()
    course_id = scrapy.Field()
    class_type = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    classtimeNames = scrapy.Field()
    reg_num = scrapy.Field()
    area_name = scrapy.Field()
    servicecenterName = scrapy.Field()

    teacher_emp_no = scrapy.Field()
    teacher_id = scrapy.Field()
    teacher_name = scrapy.Field()
    #teacher_picture_url = scrapy.Field()  太长了没什么用

    tutor_emp_no = scrapy.Field()
    tutor_id = scrapy.Field()
    tutor_sys_name = scrapy.Field()
    #tutor_picture_url = scrapy.Field()

    business_type = scrapy.Field()
    max_persons = scrapy.Field()
    surplus_persons = scrapy.Field()
    class_count = scrapy.Field()
    venue_name = scrapy.Field()
    price = scrapy.Field()
    fee_type = scrapy.Field()
    classroom_name = scrapy.Field()
    biz_type = scrapy.Field()
    cla_quota_num = scrapy.Field()
    cla_quota_state = scrapy.Field()

    course_reg_num = scrapy.Field()

    class_resist_state = scrapy.Field()
    class_resist_state_num = scrapy.Field()
    district_id = scrapy.Field()
    district_name = scrapy.Field()

    subject_id = scrapy.Field()
    subject_name = scrapy.Field()

    level_name = scrapy.Field()


    #保存切割下来的整条文件
    #json = scrapy.Field()
    snapshot_time = scrapy.Field()



#后面是详情页的item


class classItem(scrapy.Item):
    table = "classes"

    course_id = scrapy.Field()
    class_number = scrapy.Field()
    class_name = scrapy.Field()
    course_time = scrapy.Field()


    start_time = scrapy.Field() #
    end_time = scrapy.Field()
    snapshot_time = scrapy.Field()
