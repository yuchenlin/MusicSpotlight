#coding=utf-8
import api
import jieba
from bs4 import BeautifulSoup
import os
import sys
import re
reload(sys)
sys.setdefaultencoding("utf-8")

def ProcessOneMusic(musicID):
	
 	'''
 	metas 
 	0 歌名 
 	1 歌手 
 	2 专辑名 
 	3 歌曲介绍
 	'''

 	metas = []
 	
 	try:
	 	if(not os.path.exists('basic_info/'+musicID+'.txt')):
	 	#if(1):
	 		htmlFile = 'html/'+ musicID+'.html'
			f = open(htmlFile,'r')
			html = f.read()
			f.close()
		 	bs = BeautifulSoup(html,'html.parser')

		 	description = bs.find('meta',{'name':'description'})['content']
		 	title = bs.title.string
		 	if(len(title.split(' - '))==0):
		 		return
	 		metas.append(title.split(' - ')[0])
		 	metas.append(title.split(' - ')[1])
		 	begin = description.find('所属专辑：')#获取专辑名称
		 	end = description.find('。',begin)
		 	metas.append(description[begin+5:end])
		 	if('网易云音乐' not in description):
		 		metas.append(" ".join(jieba.cut(description.replace('\n',''))))
		 	else:
		 		metas.append("no description")
		 	f = open('basic_info/'+musicID+'.txt','w')
		 	for m in metas:
		 		if(m==None): 
		 			m = " ";
		 		f.write(m.encode('utf8')+'\n')
		 	f.close()
		if(not os.path.exists('lrc_jieba/'+musicID+'.txt')):
		 	lrc = api.saveLyrics(musicID)
		 	if(lrc != None):
		 		f = open('lrc_jieba/'+musicID+'.txt','w')
		 		lrc = re.sub(r"\[.*?\]", "", lrc)#删除时间
		 		lrc = " ".join(jieba.cut(lrc))#分词
		 		if(lrc==None):
		 			lrc = ' '
		 		f.write(lrc.encode('utf8')+'\n')
		 		f.close()
		global count
		print count,musicID,'OK'
		count+=1
	except Exception,e:
		print e
		print count,musicID,'Not OK'
		return
lst = []
count = 1
f = open('index.txt','r')
lines = f.xreadlines()
for l in lines:
    lst.append(l[:l.find('.')])
f.close()
import time
from multiprocessing import Pool
from multiprocessing.dummy import Pool as TPool
start = time.time()
p = TPool(30)
p.map(ProcessOneMusic,lst)
p.close()
p.join()
print time.time() - start


#ProcessOneMusic('5263227')

