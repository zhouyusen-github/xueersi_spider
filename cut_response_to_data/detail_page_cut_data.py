
import re
def detail_page_information(html_content):
    course_content = re.search('<script>window.__NUXT__=\((.*?)\);</script>', html_content).group(1)
    # 获取变量部分

    function_variables = re.findall('function\((.*?)\)', course_content)
    # 获取变量字母
    variable_characters = re.findall('(.*?),', function_variables[0])
    # 获取变量实际值
    function_facts = re.findall('}\((.*?)\)', course_content)
    variable_facts = re.findall('(.*?),', function_facts[0])
    # variable_facts = [i.replace('\"', '') for i in variable_facts]#去除双引号
    characters_to_facts = dict(zip(variable_characters, variable_facts))

    # 变量替换为实际值,实际证明替换后双引号也会一并进入字段，因为findall时双引号已是字符串的一部分
    for i in variable_characters:
        # 这里好多例外要处理真的，而且还有性能问题，用接口会更舒服,
        course_content = course_content.replace((":" + i + ","), (":" + characters_to_facts[i] + ","))
        course_content = course_content.replace((":" + i + "}"), (":" + characters_to_facts[i] + "}"))
        course_content = course_content.replace((":" + i + ";"), (":" + characters_to_facts[i] + ";"))
        course_content = course_content.replace(("=" + i + ","), ("=" + characters_to_facts[i] + ","))
        course_content = course_content.replace(("=" + i + "}"), ("=" + characters_to_facts[i] + "}"))
        course_content = course_content.replace(("=" + i + ";"), ("=" + characters_to_facts[i] + ";"))

    #print(citys_content)
    return course_content

'''
schedule:[
            {
                name:"（11.6）C阶第一讲",
                course_time:"11\u002F06 (周三) 18:30-20:00",
                is_end:"1"
            },
            {
                name:"（11.13）C阶第二讲",
                course_time:"11\u002F13 (周三) 18:30-20:00",
                is_end:"0"
            },
            {
                name:"（11.20）C阶第三讲",
                course_time:"11\u002F20 (周三) 18:30-20:00",
                is_end:"0"
            }]


'''
def cut_classes(course_content):
    classes_together = re.search('schedule:[(.*?)]', course_content).group(1)
    class_conents = re.findall('{(.*?)}', classes_together)
    return class_conents


'''
{
                name:"（11.6）C阶第一讲",
                course_time:"11\u002F06 (周三) 18:30-20:00",
                is_end:"1"
            }
'''
from xueersi_py_test.items import classItem
def cut_class_detail(class_conent,course_id,class_number):
    item = classItem()

    item['course_id'] = course_id
    item['class_number'] = class_number
    item['class_name'] = re.search('name:"(.*?)"', class_conent).group(1)
    item['course_time'] = re.search('course_time:"(.*?)"', class_conent).group(1)


    pass
