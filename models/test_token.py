import datetime
import time
import urllib.request
import json
import requests

access_token = ''


def get_token():
    '''获取钉钉的token
    :return: 钉钉token'''

    appkey = 'dingtvtbzlvg3tniqrlw'
    appsecret = 'OU8_YMl34gJici3N7cCQeJOqq8Ego08GJ-Y9f_6xwClpa1I6QzTAi9s9Swpa9VNc'
    global access_token
    headers = {
        'Content-Type': 'application/json',
    }
    url = 'https://oapi.dingtalk.com/gettoken?appkey=%s&appsecret=%s' % (appkey, appsecret)
    req = requests.get(url, headers=headers)
    result = json.loads(req.text)
    access_token = result.get('access_token')


def get_department():
    dept_ids = []
    dept_names = []
    headers = {
        'Content-Type': 'application/json',
    }
    url = 'https://oapi.dingtalk.com/department/list?access_token=%s' % (access_token)
    req = requests.get(url, headers=headers)
    result = json.loads(req.text)
    result_json = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False)  # 以json的格式输出
    # print(result_json)
    dept_name_list = result.get('department')
    i = 0
    for dept_name in dept_name_list:
        if dept_name:
            dept_ids.append(dept_name_list[i]['id'])
            dept_names.append(dept_name_list[i]['name'])
            i += 1
        else:
            print()
    # print(dept_ids)
    # print(dept_names)
    return dept_ids, dept_names


def get_department_user():
    headers = {
        'Content-Type': 'application/json',
    }
    department_id_list, department_name_list = get_department()
    id_list = []
    name_list = []
    dept_id_name_list = dict(zip(department_id_list, department_name_list))
    dept_name_list = []
    dept_id_list = []
    for department in department_id_list:
        department_id = department
        url = 'https://oapi.dingtalk.com/user/listbypage?access_token=%s&department_id=%s&offset=0&size=100' % (
            access_token, department_id)
        req = requests.get(url, headers=headers)
        list1 = json.loads(req.text)
        userlist = list1.get('userlist')

        i = 0
        for user in userlist:
            for key in dept_id_name_list:
                if department_id == key:
                    dept_name_list.append(dept_id_name_list[key])
                    dept_id_list.append(department_id)
            if user:
                id_list.append(userlist[i]['userid'])
                name_list.append(userlist[i]['name'])
                i += 1
            else:
                print()

    # print(id_list)
    # print(name_list)
    # print(dept_id_list)
    # print(dept_name_list)
    return id_list, name_list, dept_name_list, dept_id_list


def get_users_name():
    users_id = get_users_id()
    headers = {
        'Content-Type': 'application/json',
    }
    users_name = []
    for user_id in users_id:
        url = 'https://oapi.dingtalk.com/user/get?access_token=%s&userid=%s' % (access_token, user_id)
        req = requests.get(url, headers=headers)
        list1 = json.loads(req.text)
        users_name.append(list1['name'])
    # print(users_id)
    # print(users_name)
    return users_id, users_name


def get_users_id():
    dept_ids, dept_names = get_department()
    headers = {
        'Content-Type': 'application/json',
    }
    user_ids = []
    for dept_id in dept_ids:
        url = 'https://oapi.dingtalk.com/user/getDeptMember?access_token=%s&deptId=%s' % (access_token, dept_id)
        req = requests.get(url, headers=headers)
        list1 = json.loads(req.text)
        user_ids += list1['userIds']
    return user_ids


def get_attendance_list():
    user_ids = get_users_id()
    headers = {
        "workDateFrom": "2019-12-24 00:00:00",
        "workDateTo": "2019-12-30 00:00:00",
        "userIdList": user_ids,
        "offset": "0",
        "limit": "50"
    }
    url = 'https://oapi.dingtalk.com/attendance/list?access_token=%s' % (access_token)
    req = requests.post(url, json.dumps(headers))
    result = json.loads(req.text)
    userlist = result.get('recordresult')
    result1_json = json.dumps(userlist, indent=2, sort_keys=True, ensure_ascii=False)  # 以json的格式输出
    # print(result1_json)
    return userlist


def get_parent_ids():
    dept_ids, dept_names = get_department()
    parent_list = []
    headers = {
        'Content-Type': 'application/json',
    }
    for dept_id in dept_ids:
        url = 'https://oapi.dingtalk.com/department/list_parent_depts_by_dept?access_token=%s&id=%s' % (
            access_token, dept_id)
        req = requests.get(url, headers=headers)
        result = json.loads(req.text)
        parent_list.append(result)
        result_json = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False)  # 以json的格式输出
    # print(parent_list)

    return parent_list


get_token()
get_department()
get_department_user()
get_users_id()
get_users_name()
get_attendance_list()
get_parent_ids()
