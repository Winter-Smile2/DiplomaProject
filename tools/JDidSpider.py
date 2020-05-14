#-*-coding:utf-8-*-
"""
    爬取京东手机产品ID
"""
from urllib import parse
from selenium import webdriver
import time

options = webdriver.ChromeOptions()
# 添加无界面参数
options.add_argument('--headless')
# browser = webdriver.Chrome()
# browser.get('https://shouji.jd.com/')
# browser.find_element_by_xpath('//*[@id="key"]').send_keys('努比亚红魔3')
# browser.find_element_by_xpath('//*[@class="button cw-icon"]').click()
# time.sleep(2)
# browser.find_element_by_xpath('//ul[@class="gl-warp clearfix"]/li[1]//a[1]').click()
# browser.switch_to.window(browser.window_handles[1])
# time.sleep(5)
# print(browser.page_source)
# url00 = browser.current_url
# print(url00)
# browser.quit()
url = 'https://item.jd.com/100011513372.html?kw={}'
print(url.format(2))