#-*-coding:utf-8-*-
# 有关手机评论的爬虫
import os

from fake_useragent import UserAgent
import requests
from queue import Queue
import time
import csv
from threading import Lock,Thread
from urllib import parse

from lxml import etree
from selenium import webdriver
import json

class CommentSpider:
    def __init__(self,product):
        self.root_url = 'https://shouji.jd.com/'
        # 产品名称
        self.product = product
        # 评论网页地址
        self.page_url = 'https://club.jd.com/comment/skuProductPageComments.action?productId={}&score=0&sortType=5&page=1'
        # 官方网址
        self.url = 'https://club.jd.com/comment/skuProductPageComments.action?productId={}&score=0&sortType=5&page={}'
        # 评论存储地址
        self.addr = 'dog.csv'
        self.q = Queue()
        self.lock = Lock()
        # 存放所有数据的大列表,用于writerows()方法
        self.item_list = []
        self.i = 0
        self.f = open(self.addr, 'w',newline='')
        self.writer = csv.writer(self.f,delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    # 获取指定手机型号ID
    def get_teleID(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        browser = webdriver.Chrome(options=options)
        browser.get(self.root_url)
        browser.find_element_by_xpath('//*[@id="key"]').send_keys(self.product)
        browser.find_element_by_xpath('//*[@class="button cw-icon"]').click()
        time.sleep(2)
        browser.find_element_by_xpath('//ul[@class="gl-warp clearfix"]/li[1]//a[1]').click()
        browser.switch_to.window(browser.window_handles[1])
        ProductId = browser.current_url[20:-5]
        browser.quit()
        return ProductId
    # 获取指定页面内容
    def get_html(self,url):
        header = {'User-Agent':UserAgent().random}
        html = requests.get(url,headers=header).json()
        return html
    # 获取总页数
    def get_total(self):
        productId = self.get_teleID()
        page_url = self.page_url.format(productId)
        html = requests.get(url=page_url, headers={'User-Agent': UserAgent().random}).json()
        count = html['productCommentSummary']['commentCount']
        numbers = int(count)
        if numbers % 10 == 0:
            total = numbers // 10
        else:
            total = numbers // 10 + 1
        return total
    # 入队列
    def url_in(self):
        # keyword = input('请输入手机名称:')
        # keyword = parse.quote(keyword)
        total = self.get_total()
        productId = self.get_teleID()
        for page in range(0, 100):
            url = self.url.format(productId,page)
            # print(url)
            self.q.put(url)
    # 提取评论，线程事件函数
    def parse_page(self):
        while True:
            if not self.q.empty():
                url = self.q.get()
                # html = json.loads(self.get_html(url))
                html = self.get_html(url)
                comments = html['comments']
                for comment in comments:
                    try:
                        # 评论
                        item = {}
                        item['comment'] = comment['content']
                        # 写入csv文件数据类型: [(),(),(),...,()]
                        item_tuple = (item['comment'])
                        self.item_list.append(item_tuple)
                        print(item)
                        self.lock.acquire()
                        self.i += 1
                        self.lock.release()
                    except Exception as e:
                        break
            else:
                break

    def run(self):
        self.url_in()
        t_list = []
        for i in range(3):
            t = Thread(target=self.parse_page)
            time.sleep(2)
        t_list.append(t)
        t.start()
        for t in t_list:
            t.join()
        print('数量:', self.i)
        # 将所有数据一次性写入文件
        self.writer.writerows(self.item_list)
        self.f.close()
class TiebaSpdider:
    def __init__(self,product):
        self.url = 'https://tieba.baidu.com/f?kw={}&pn={}'
        self.i = 0
        self.q = Queue()
        self.lock = Lock()
        self.addr = 'dog.csv'
        # 存放所有数据的大列表,用于writerows()方法
        self.item_list = []
        self.i = 0
        self.f = open(self.addr, 'a', newline='')
        self.writer = csv.writer(self.f,delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        self.product = product
    # 获取页面内容
    def get_html(self,url):
        header = {'User-Agent':UserAgent().random}
        html = requests.get(url,headers=header).text
        return html

    # 获取总页数
    def get_total(self):
        url = self.url.format(self.product,50)
        html = self.get_html(url)
        html_new = html.replace(r'<!--','').replace(r'-->','')
        p = etree.HTML(html_new)
        total = p.xpath('//*[@id="frs_list_pager"]/a[last()]/@href')[0][56:]
        print(total)
        total = int(total)
        return total

    # 入队列
    def url_in(self):
        total = self.get_total()+1
        for page in range(0,total,50):
            url = self.url.format(self.product,page)
            self.q.put(url)
    # 解析函数，线程函数
    def parse_page(self):
        while True:
            if not self.q.empty():
                url = self.q.get()
                html = self.get_html(url)
                html_new = html.replace(r'<!--', '').replace(r'-->', '')
                content = etree.HTML(html_new)
                li_list = content.xpath('//ul[@id="thread_list"]//li')
                print(li_list)
                for li in li_list:
                    try:
                        # 评论
                        item = {}
                        item['comment'] = li.xpath('.//div[@class="threadlist_abs threadlist_abs_onlyline "]/text()')
                        if item['comment'] == []:
                            continue
                        item['comment'] = item['comment'][0].strip()
                        # 写入csv文件数据类型: [(),(),(),...,()]
                        item_tuple = (item['comment'])
                        self.item_list.append(item_tuple)
                        print(item)
                        self.lock.acquire()
                        self.i += 1
                        self.lock.release()
                    except Exception as e:
                        print(e)
                        break
            else:
                break
    # 运行
    def run(self):
        self.url_in()
        t_list = []
        for i in range(3):
            t = Thread(target=self.parse_page)
            time.sleep(2)
        t_list.append(t)
        t.start()
        for t in t_list:
            t.join()
        print('数量:', self.i)
        # 将所有数据一次性写入文件
        self.writer.writerows(self.item_list)
        self.f.close()
if __name__ == '__main__':
    # -----------------------京东--------------------------------------
    product = input('请输入手机型号:')
    # cs = CommentSpider(product)
    # cs.run()
    # -----------------------------------------------------------------
    time.sleep(2)
    tb = TiebaSpdider(product)
    tb.run()