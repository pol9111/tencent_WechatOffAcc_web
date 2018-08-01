from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from pprint import pprint
from time import sleep
import json

# 登入时上传的参数
post = {}
url = 'https://mp.weixin.qq.com/'
# 微信公众号, 注意不是微信个人账户
account = ''
passwd = ''

# 自动化测试
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
driver.get(url)
sleep(3)
driver.find_element_by_xpath('./*//input[@name="account"]').clear()
driver.find_element_by_xpath('./*//input[@name="account"]').send_keys(account)
driver.find_element_by_xpath('./*//input[@name="password"]').clear()
driver.find_element_by_xpath('./*//input[@name="password"]').send_keys(passwd)

# sleep(5)
driver.find_element_by_xpath('./*//a[@class="btn_login"]').click()

sleep(10)
driver.get(url)
cookie_items = driver.get_cookies()
pprint(cookie_items)

for cookie_item in cookie_items:
    post[cookie_item['name']] = cookie_item['value']

# 保存cookies
cookies_str = json .dumps(post)
with open('cookies.txt', 'w+', encoding='utf-8') as f:
    f.write(cookies_str)





