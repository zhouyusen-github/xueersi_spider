# -*- coding: utf-8 -*-
import re
from xueersi_py_test.items import CityItem,gradeItem,coursesTotalCountItem,courseItem
import time
#本py专门用于将返回切割成item形式

#1.city切割
#切割city条目
def cut_city(html_content):
    # 观察可得网页最后的script含有所有城市信息，顺序和网页相同，但是部分用a,b,c隐藏在变量里，需要先把变量填回去
    # 截取nuxt script部分
    citys_content = re.search('<script>window.__NUXT__=\((.*?)\);</script>', html_content).group(1)
    # 获取变量部分
    function_variables = re.findall('\((.*?)\)', citys_content)
    # 获取变量字母
    variable_characters = re.findall('(.*?),', function_variables[0])
    # 获取变量实际值
    variable_facts = re.findall('(.*?),', function_variables[1])
    # variable_facts = [i.replace('\"', '') for i in variable_facts]#去除双引号
    characters_to_facts = dict(zip(variable_characters, variable_facts))

    # 变量替换为实际值,实际证明替换后双引号也会一并进入字段，因为findall时双引号已是字符串的一部分
    for i in variable_characters:
        # 这里好多例外要处理真的，而且还有性能问题，用接口会更舒服,
        citys_content = citys_content.replace((":" + i + ","), (":" + characters_to_facts[i] + ","))
        citys_content = citys_content.replace((":" + i + "}"), (":" + characters_to_facts[i] + "}"))
        citys_content = citys_content.replace((":" + i + ";"), (":" + characters_to_facts[i] + ";"))
        citys_content = citys_content.replace(("=" + i + ","), ("=" + characters_to_facts[i] + ","))
        citys_content = citys_content.replace(("=" + i + "}"), ("=" + characters_to_facts[i] + "}"))
        citys_content = citys_content.replace(("=" + i + ";"), ("=" + characters_to_facts[i] + ";"))

    citys_content = re.search('\){(.*?);return', citys_content).group(1)
    # 上面这一步处理完就和接口的数据一样了
    print(citys_content)
    citys = re.findall('{(.*?)}', citys_content)

    for i in range(len(citys)):
        citys[i] = "{" + citys[i] + "}"  # 为了后面可以识别出local_city

    return citys
#切割各city条目详细信息
def cut_city_detail(city):
    item = CityItem()
    item['id'] = re.search('id:(.*?),', city).group(1)
    item['name'] = re.search('name:"(.*?)",', city).group(1)
    item['area'] = re.search('area:"(.*?)",', city).group(1)
    item['pinyin'] = re.search('pinyin:"(.*?)",', city).group(1)
    item['local_city'] = re.search('local_city:"(.*?)"}', city).group(1)
    item['snapshot_time'] = snapshot_time()
    return item

'''-----------------------------------------------------------------------------------------------------------------'''
#切割有哪些年级及详细信息
def cut_grade_list(string):#切割出每个年级
    frontParts = re.findall('{"grd_id"(.*?)"cla_gt_name"', string)
    backParts = re.findall('"cla_gt_name"(.*?)}', string)
    grade_list = []
    for i in range(len(frontParts)):
        course_status = '{"grd_id"' + frontParts[i] + '"cla_gt_name"' + backParts[i] + "}"
        grade_list.append(course_status)
    return (grade_list)

def cut_grade_list_detail(string,name,areaCode):#切割出年级详细信息
    item = gradeItem()
    item['grd_id'] = findInString("grd_id", 0, string)
    item['grd_name'] = findInString("grd_name", 0, string)
    item['cla_gt_id'] = findInString("cla_gt_id", 0, string)
    item['cla_gt_name'] = findInString("cla_gt_name", 0, string)

    item['name'] = name
    item['areaCode'] = areaCode
    item['snapshot_time'] = snapshot_time()
    return item


'''------------------------------------------------------------------------------------------------------------------'''
#3.切割网页课程总条目数
def cut_courses_totalcount(string,name,areaCode,grd_id,grd_name):
    item = coursesTotalCountItem()
    item['name'] = name
    item['areaCode'] = areaCode
    item['grd_id'] = grd_id
    item['grd_name'] = grd_name





    item['status'] = findInString("status", 1, string)
    item['code'] = findInString("code", 1, string)
    item['msg'] = findInString("msg", 0, string)
    item['totalCount'] = int(findInString("totalCount", 1, string))

    item['name'] = name
    item['areaCode'] = areaCode
    item['snapshot_time'] = snapshot_time()
    return item

'''-----------------------------------------------------------------------------------------------------------------'''
#4.切割课程详细信息
#将接口内10条数据切开
def cut_course_status(string):
    frontParts = re.findall('{"class_id"(.*?)"level_name"',string)
    backParts = re.findall('"level_name"(.*?)}', string)
    courses_status = []
    for i in range(len(frontParts)):
        course_status = '{"class_id"'+frontParts[i] + '"level_name"' + backParts[i] + "}"
        #print(course_status)
        courses_status.append(course_status)
    return(courses_status)

#把每条数据的各字段提取出来
def course_status_to_courseItem(string,cityName,cityCode,gradeName,gradeId):
    item = courseItem()

    item['cityName'] = cityName
    item['cityCode'] = cityCode
    item['gradeName'] = gradeName
    item['gradeId'] = gradeId


    item['class_id'] = findInString("class_id", 0, string)
    item['class_name'] = findInString("class_name", 0, string)
    item['course_id'] = findInString("course_id", 0, string)
    item['class_type'] = intsql(findInString("class_type", 0, string))
    item['start_date'] = findInString("start_date", 0, string)
    item['end_date'] = findInString("end_date", 0, string)
    item['classtimeNames'] = findInString("classtimeNames", 0, string)
    item['reg_num'] = findInString("reg_num", 1, string)
    item['area_name'] = findInString("area_name", 0, string)
    item['servicecenterName'] = findInString("servicecenterName", 0, string)
    item['teacher_emp_no'] = findInString("teacher_emp_no", 0, string)
    item['teacher_id'] = findInString("teacher_id", 0, string)
    item['teacher_name'] = findInString("teacher_name", 0, string)
    #item['teacher_picture_url'] = findInString("teacher_picture_url", 0, string)
    item['tutor_emp_no'] = findInString("tutor_emp_no", 0, string)
    item['tutor_id'] = findInString("tutor_id", 0, string)
    item['tutor_sys_name'] = findInString("tutor_sys_name", 0, string)
    #item['tutor_picture_url'] = findInString("tutor_picture_url", 0, string)
    item['business_type'] = intsql(findInString("business_type", 0, string))

    item['max_persons'] = intsql(findInString("max_persons", 1, string))
    item['surplus_persons'] = intsql(findInString("surplus_persons", 1, string))
    item['class_count'] = intsql(findInString("class_count", 1, string))

    item['venue_name'] = findInString("venue_name", 0, string)
    item['price'] = intsql(findInString("price", 0, string))
    item['fee_type'] = intsql(findInString("fee_type", 0, string))
    item['classroom_name'] = findInString("classroom_name", 0, string)
    item['biz_type'] = intsql(findInString("biz_type", 0, string))
    item['cla_quota_num'] = findInString("cla_quota_num", 0, string)
    item['cla_quota_state'] = intsql(findInString("cla_quota_state", 0, string))

    item['course_reg_num'] = intsql(findInString("course_reg_num", 1, string))
    item['class_resist_state'] = intsql(findInString("class_resist_state", 1, string))
    item['class_resist_state_num'] = intsql(findInString("class_resist_state_num", 1, string))

    item['district_id'] = findInString("district_id", 0, string)
    item['district_name'] = findInString("district_name", 0, string)
    item['subject_id'] = findInString("subject_id", 0, string)
    item['subject_name'] = findInString("subject_name", 0, string)
    item['level_name'] = findInString("level_name", 0, string)

    #item['json'] = string
    item['snapshot_time'] = snapshot_time()
    return item

'''
#测试course_status_to_courseItem函数
string = '{"class_id":"37e1e436b5ce4a74819edea67b8c9f58","class_name":"秋季班小学三年级英语培训班(创新)","course_id":"0101-DTF6sxHu1cZFWV7zRs94Qx","class_type":"2","start_date":"2019-09-07","end_date":"2019-12-30","classtimeNames":"周六晚上18:00-20:30","reg_num":11,"area_name":"南海区","servicecenterName":"南桂路服务中心","teachers":[{"teacher_emp_no":"011961","teacher_id":"a6040efea21e4275b4ad7b9e309a69de","teacher_name":"麦碧珊","teacher_picture_url":"http://teacher-center-avator.oss-cn-beijing.aliyuncs.com/image/20180912/6edbc618-536b-4e1b-b9db-e6ec98f2046e.jpg"}],"tutors":[{"tutor_emp_no":"139121","tutor_id":"9fdaf22a4b6e4d07a04972a5ca8647fa","tutor_sys_name":"陈方芳139121","tutor_picture_url":"http://teacher-center-avator.oss-cn-beijing.aliyuncs.com/image/20190711/174ec46d-c122-44d6-985e-ef3c3c5602d6.jpg"}],"business_type":"0","max_persons":18,"surplus_persons":7,"class_count":15,"venue_name":"南海区城市广场","price":"3170","fee_type":"2","classroom_name":"城市广场301","biz_type":"0","cla_quota_num":"热报","cla_quota_state":"3","class_resist_state":4,"class_resist_state_num":0,"district_id":"440605","district_name":"南海区","subjects":[{"subject_id":"ff80808127d77caa0127d7e164bd00c8","subject_name":"英语"}],"level_name":"培训班(创新)"}'

answer = course_status_to_courseItem(string)
print(answer)
'''

'''-----------------------------------------------------------------------------------------------------------------'''
#常用函数
#包装一个函数用于处理返回none,findall和search各有缺点，所以自己写一个更好,目的有值返回值，无值返回none
def findInString(name,isint,string):#int和string的搜索正则不同,用isint控制
    if isint:
        answer = re.search('"'+name+'":(.*?),', string)
    else:
        answer = re.search('"'+name+'":"(.*?)"', string)

    if answer:#search无结果返回none，对应布尔是false
        return answer.group(1)
    else:
        return answer
'''
def intsql(string):#为了应付int空值情况，int()函数会报错
    if string == 0:
        return 0
    if string: #包含了"0"的情况
        return int(string)
    else:#处理none等情况，毕竟数据库int存入空值会报错
        return -9999
'''
#更换回原模块，因为mysql数据库是可以介绍 int default null的（但是还是要避免）
def intsql(string):
    if string == 0:
        return 0
    if string:  # 包含了"0"的情况
        return int(string)
    else:  # 处理none
        return string#这样可以把none给数据库，数据库会处理成null的



import datetime
def snapshot_time(): #这个以后可能对时间格式做修改，所以独立出来
    #return str(time.time())
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")#这个未测试
    return dt



