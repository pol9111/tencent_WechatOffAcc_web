from config import *
import requests, random, time

def search_off_acc(headers, cookies, token, search_url):
    # 要爬取的公众号列表, 最好用公众号的ID, 中文名字爬取的有可能不是你想要的那个
    official_acc = ['JOKER-1943']

    # 循环爬取列表里的每个公众号
    for query in official_acc:
        query_id = {
            'action': 'search_biz',
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'query': query,
            'begin': '0',
            'count': '5',
        }

        # 在搜索接口搜索某公众号的url构造
        search_rs = requests.get(search_url, headers=headers, cookies=cookies, params=query_id)

        # 获取公众号的fakeid
        acc_lst = search_rs.json().get('list')[0]
        fakeid = acc_lst.get('fakeid')
        return fakeid

def enter_off_acc(headers, cookies, token, fakeid, appmsg_url):
    query_id_data = {
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'action': 'list_ex',
        'begin': '0',
        'count': '5',
        'query': '',
        'fakeid': fakeid,
        'type': '9'
    }

    # 点击某个公众号, 进入公众号文章列表的url构造
    appmsg_rs = requests.get(appmsg_url, headers=headers, cookies=cookies, params=query_id_data)

    # 总文章数app_msg_cnt / 5 可知要翻多少页
    max_num = appmsg_rs.json().get('app_msg_cnt')
    num = int(int(max_num) / 5)
    return num

def get_each_page(headers, cookies, token, fakeid, appmsg_url, num, table):
    begin = 0

    # 循环爬取某个公众号的每一页
    while num + 1 > 0:
        query_id_data = {
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'action': 'list_ex',
            'begin': '{}'.format(str(begin)),
            'count': '5',
            'query': '',
            'fakeid': fakeid,
            'type': '9'
        }
        acc_eachpage_rs = requests.get(appmsg_url, headers=headers, cookies=cookies, params=query_id_data)
        article_list = acc_eachpage_rs.json().get('app_msg_list')
        # 循环保存每一页文章
        for item in article_list:
            title = item.get('title')
            link = item.get('link')
            update_time = item.get('update_time')
            data = {
                '文章标题': title,
                '文章链接': link,
                '发布时间': update_time,
            }
            print(data)
            table.update({'文章标题': title}, {'$set': data}, True)
        num -= 1
        begin += 5
        time.sleep(15)
        print('next_page' + '-'*20 + '\n'*3)

if __name__ == '__main__':
    while True:
        FAKEID = search_off_acc(HEADERS, COOKIES, TOKEN, SEARCH_URL)
        NUM = enter_off_acc(HEADERS, COOKIES, TOKEN, FAKEID, APPMSG_URL)
        get_each_page(HEADERS, COOKIES, TOKEN, FAKEID, APPMSG_URL, NUM, TABLE)



