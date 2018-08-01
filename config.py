import pymongo, json, requests, re

# mongodb的配置
CLIENT = pymongo.MongoClient('localhost')
DB = CLIENT['wechat']
TABLE = DB['off_acc_PC']

URL = 'https://mp.weixin.qq.com'
HEADERS = {
    "HOST": "mp.weixin.qq.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
}

# 获取事先保存的cookies  cookies有实效, 拿不到token, 再获取一次cookies
with open('cookies.txt', 'r', encoding='utf-8') as f:
    cookies_js = f.read()

# 登入以获取token
COOKIES = json.loads(cookies_js)
rs = requests.get(url=URL, headers=HEADERS, cookies=COOKIES)
TOKEN = re.findall(r'token=(\d+)', str(rs.url))[0]

# 在搜索接口搜索某公众号的url
SEARCH_URL = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'

# 点击某个公众号, 进入公众号文章列表的url
APPMSG_URL = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'




