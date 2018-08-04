from config import *
import requests, random, time

class Spider():
    def __init__(self):
        self.headers = HEADERS
        self.cookies = COOKIES
        self.token = TOKEN
        self.search_url = SEARCH_URL
        self.appmsg_url = APPMSG_URL
        self.table = TABLE

    @classmethod
    def search_off_acc(cls):
        # 要爬取的公众号列表
        official_acc = ['JOKER-1943']

        # 循环爬取列表里的每个公众号
        for query in official_acc:
            query_id = {
                'action': 'search_biz',
                'token': TOKEN,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': '1',
                'random': random.random(),
                'query': query,
                'begin': '0',
                'count': '5',
            }

            # 在搜索接口搜索某公众号的url构造
            search_rs = requests.get(SEARCH_URL, headers=HEADERS, cookies=COOKIES, params=query_id)

            # 获取公众号的fakeid
            acc_lst = search_rs.json().get('list')[0]
            FAKEID = acc_lst.get('fakeid')
            return FAKEID

    @classmethod
    def enter_off_acc(cls, fakeid):
        query_id_data = {
            'token': TOKEN,
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
        appmsg_rs = requests.get(APPMSG_URL, headers=HEADERS, cookies=COOKIES, params=query_id_data)

        # 总文章数app_msg_cnt / 5 可知要翻多少页
        max_num = appmsg_rs.json().get('app_msg_cnt')
        NUM = int(int(max_num) / 5)
        return NUM

    @classmethod
    def get_each_page(cls, fakeid, num):
        begin = 0

        # 循环爬取某个公众号的每一页
        while num + 1 > 0:
            query_id_data = {
                'token': TOKEN,
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
            acc_eachpage_rs = requests.get(APPMSG_URL, headers=HEADERS, cookies=COOKIES, params=query_id_data)
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
                TABLE.update({'文章标题': title}, {'$set': data}, True)
            num -= 1
            begin += 5
            time.sleep(15)
            print('next_page' + '-'*20 + '\n'*3)


if __name__ == '__main__':
    spider = Spider() # 创建一个微信爬虫
    fakeid = spider.search_off_acc() # 搜索公众号, 获取公众号的fakeid
    num = spider.enter_off_acc(fakeid) # 点击进入公众号, 获取页码num
    spider.get_each_page(fakeid, num) # 循环翻页, 获取公众号的所有文章



