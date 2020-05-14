from django.shortcuts import render

# Create your views here.

# -*-coding:utf-8-*-
"""
    爬取识微科技的关于手机舆情的文章链接、图片、名称
"""
from django.http import JsonResponse
from queue import Queue
from threading import Thread, Lock
from urllib import request
import time
import random
from lxml import etree
import re
from fake_useragent import UserAgent
import requests
import pymysql
import json
q = Queue()
lock = Lock()
n = 0

# 获取页面内容
def get_html(url, header):
    headers = header
    req = request.Request(url=url, headers=headers)
    resp = request.urlopen(req)
    html = resp.read().decode('utf-8')
    return html

# html = html.decode('utf-8')
# pat = '<div class="broadcast-item">.*?src="(.*?)".*?href="(.*?)"'
# pattern = re.compile(pat,re.S|re.M)
# res_list = pattern.findall(html01)
# print(res_list)
# print(html)
# 保存链接、图片和标题到本地
def save_data(link_list, db):
    global n
    # https://www.civiw.com/business/20200421145524
    # https://www.civiw.com/image/c314835a-cfa0-44f6-bed9-7c51ac0ed256
    url = 'https://www.civiw.com'
    cursor = db.cursor()
    for i in range(len(link_list)):
        img_link = url+link_list[i]['img_link'][0]
        headers = {'User-Agent': UserAgent().random}
        image = requests.get(url=img_link, headers=headers).content
        href_link = url+link_list[i]['href'][0]
        title = link_list[i]['title'][0]
        filename = '/home/winter/Desktop/Python/client/static/images/'+'baner0'+str(n+1)+'.jpg'
        tag_name = link_list[i]['tag_name']
        tag_name_str = ''
        print(len(tag_name))
        for j in range(len(tag_name)):
            tag_name_str += tag_name[j]+' '
        print(tag_name_str)
        time = link_list[i]['time'][0]
        visits_num = link_list[i]['visits-num']
        n += 1
        sql = "insert into index_link(img_path,href,title,tag_name,time,visit_num) values(%s,%s,%s,%s,%s,%s)"
        lock.acquire()
        with open(filename,'wb') as f:
            f.write(image)
        cursor.execute(sql,[filename,href_link,title,tag_name_str,time,visits_num])
        db.commit()
        lock.release()
    print(link_list)
# 解析页面内容
def parse_html(html,db):
    parse = etree.HTML(html)
    # img_link = parse_html.xpath('//div[@class="broadcast-item-image"]/img/@src')
    # print(img_link)
    div_list = parse.xpath('//div[@class="broadcast-list"]/div')
    link_list = []
    for div in div_list:
        # 因为每次添加的都是同一个内存到list中去了,mydict每次写入的时候改变了内存中的value,但是地址不变,即是,创建了一次内存空间,
        # 只会不断的改变value了,添加到list中的时候value已经改了。所以需要在for循环里面去每次循环都创建一个空的dict，以保证之前
        # 添加过的不会被改变。
        item = {}
        item['img_link'] = div.xpath('.//div[@class="broadcast-item-image"]/img/@src')
        item['href'] = div.xpath('.//div[@class="title"]/a/@href')
        item['title'] = div.xpath('.//div[@class="title"]/a/text()')
        item['tag_name'] = div.xpath('.//span[@class="source"]//a/text()')
        item['time'] = div.xpath('.//span[@class="time"]/text()')
        item['visits-num'] = div.xpath('.//span[@class="visits-num"]/text()')
        if item['tag_name'].count('手机舆情') == 1:
            link_list.append(item)
    save_data(link_list,db)
# 获取页面总页数
def get_total_page():
    url = 'https://www.civiw.com/business/1'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    html = get_html(url, header)
    parse = etree.HTML(html)
    page = parse.xpath('//div[@class="page-container"]/div[@class="pageItem"][last()]/a/text()')
    page = int(page[0])
    return page
# 主函数
def url_in():
    total_page = get_total_page()
    for page in range(1, total_page+1):
        url = 'https://www.civiw.com/business/'+str(page)
        # print(url)
        q.put(url)

def get_data(db):
    ua = UserAgent()
    header = {'User-Agent':ua.random}
    while True:
        if not q.empty():
            url = q.get()
            html = get_html(url,header)
            parse_html(html,db)
        else:
            break
def main():
    db = pymysql.connect('localhost','root','19970212','tple',charset='utf8')
    url_in()
    t_list = []
    for i in range(3):
        t = Thread(target=get_data,args=(db,))
        t_list.append(t)
        t.start()
    for t in t_list:
        t.join()
def conn_mysql():
    db = pymysql.connect('localhost','root','19970212','tple',charset='utf8')
    return db

def getdata(sql):
    db = conn_mysql()
    cursor = db.cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    cursor.close()
    db.commit()
    db.close()
    return res
def gettitle():
    sql = 'select title from index_link limit 5'
    res = getdata(sql)
    return res
def getimage():
    sql = 'select img_path from index_link limit 3'
    res = getdata(sql)
    return res
def get_title(request):
    if request.method == 'GET':
        res = gettitle()
        data = {'code':200}
        for i in range(len(res)):
            key = 'title'+str(i)
            data[key] = res[i][0]
        print(type(data))
        return JsonResponse(data)

def get_image(request):
    res = getimage()
    data = {}
    for i in range(len(res)):
        key = 'image' + str(i)
        data[key] = res[i][0]
    return JsonResponse(data)
def gethref():
    sql = 'select href from index_link limit 3'
    res = getdata(sql)
    return res
def get_href(request):
    res = gethref()
    data = {}
    for i in range(len(res)):
        key = 'href' + str(i)
        data[key] = res[i][0]
    return JsonResponse(data)
def linkspider():
    pass
def get_eititle(request):
    sql = 'select title from index_link limit 3,18'
    res = getdata(sql)
    data = {'code': 200}
    for i in range(len(res)):
        key = 'title' + str(i)
        data[key] = res[i][0]
    # print(data)
    return JsonResponse(data)
def get_eiimage(request):
    sql = 'select img_path from index_link limit 3,18'
    res = getdata(sql)
    data = {}
    for i in range(len(res)):
        key = 'image' + str(i)
        data[key] = res[i][0]
    # print(data)
    return JsonResponse(data)
def get_eihref(request):
    sql = 'select href from index_link limit 3,18'
    res = getdata(sql)
    data = {}
    for i in range(len(res)):
        key = 'href' + str(i)
        data[key] = res[i][0]
    # print(data)
    return JsonResponse(data)
def get_eitimer(request):
    sql = 'select time from index_link limit 3,18'
    res = getdata(sql)
    data = {}
    for i in range(len(res)):
        key = 'timer' + str(i)
        data[key] = res[i][0]
    # print(data)
    return JsonResponse(data)
def get_eivisits(request):
    sql = 'select visit_num from index_link limit 3,18'
    res = getdata(sql)
    data = {}
    for i in range(len(res)):
        key = 'visit' + str(i)
        data[key] = res[i][0]
    # print(data)
    return JsonResponse(data)
def get_eitally(request):
    sql = 'select tag_name from index_link limit 3,18'
    res = getdata(sql)
    data = {}
    for i in range(len(res)):
        key = 'tally' + str(i)
        data[key] = res[i][0]
    # print(data)
    return JsonResponse(data)
def get_last_image(request):
    sql = 'select img_path from index_link limit 21,13'
    res = getdata(sql)
    data = {}
    for i in range(len(res)):
        key = 'image' + str(i)
        data[key] = res[i][0]
    # print(data)
    return JsonResponse(data)
def get_last_href(request):
    sql = 'select href from index_link limit 21,13'
    res = getdata(sql)
    data = {}
    for i in range(len(res)):
        key = 'hrefs' + str(i)
        data[key] = res[i][0]
    # print(data)
    return JsonResponse(data)
def get_last_title(request):
    sql = 'select title from index_link limit 21,13'
    res = getdata(sql)
    data = {}
    for i in range(len(res)):
        key = 'tables' + str(i)
        data[key] = res[i][0]
    # print(data)
    return JsonResponse(data)
if __name__ == '__main__':
    start = time.time()
    # get_last_title()
    print('执行时间：%.2f'%(time.time()-start))

