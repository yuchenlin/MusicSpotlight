# -*- coding: utf-8 -*-
__author__ = 'Lin'

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from BeautifulSoup import BeautifulSoup
import urllib2
import time
import random
import re
import urlparse
import os
import string
import urllib
import Queue
import threading
import MyBloomFilter


def getName(s): 
    return s[29:]+".html"

def get_page(page):
    #try-catch

    try:
        html = urllib2.urlopen(page,timeout=3).read() 
    except Exception,e:
        print e,'---------',page 
        return None
    content = html
    return content 

def get_all_links(content, page):
    if content == None:
        return []
    import re
    urlset = []
    urls = re.findall(r"song\?id=[1-9]\d*",content,re.I)
    for i in urls:
        if i not in crawled:
            urlset.append('http://music.163.com/'+i)
    return urlset



def add_page_to_folder(page, content): #将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    if content==None:
        return
    try:
        index_filename = 'index.txt'    #index.txt中每行是'网址 对应的文件名'
        folder = 'html'                 #存放网页的文件夹
        filename = getName(page) #将网址变成合法的文件名
        index = open(index_filename, 'a')
        index.write(filename + ' ' + page.encode('ascii', 'ignore') + '\n')
        index.close()
        if not os.path.exists(folder):  #如果文件夹不存在则新建
            os.mkdir(folder)
        f = open(os.path.join(folder, filename), 'w')
        f.write(str(content))                #write the page into a file
        f.close()
    except Exception,e: 
        print e

def working():
    global count,crawled,max_page,q
    while count <= max_page:
        if (count==0 or q.qsize>0):
            page = q.get()
        else:
            break
        if page not in crawled:
            content = get_page(page)
            if(content!=None):
                if(count <= max_page):
                    print count,page
                    add_page_to_folder(page,content)
                    outlinks = get_all_links(content,page)
                    for link in outlinks:
                        if(q.qsize() + count > max_page):
                            break
                        q.put(link)
                    if varLock.acquire():
                        count += 1
                        crawled.append(page)
                        varLock.release()
            if q.unfinished_tasks: 
                q.task_done()
    while q.unfinished_tasks:
        if varLock.acquire():
            q.task_done()
            varLock.release()
crawled = []
count = 0
threadNUM = 30
max_page = 1000
varLock = threading.Lock()

def initCrawled():
    global crawled
    f = open('index.txt','r')
    lines = f.xreadlines()
    for l in lines:
        crawled.append(l.split()[1])
    f.close()
initCrawled()
begin = time.time()
q = Queue.Queue()
q.put('http://music.163.com/song?id=366577')
for i in range(threadNUM):
    t = threading.Thread(target = working)
    t.setDaemon(True)
    t.start()
q.join()
print time.time() - begin
