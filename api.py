#coding=utf8
import urllib
import urllib2
# print urllib2.urlopen('http://music.163.com/api/song/media?id=33469997').read()
# print urllib2.urlopen('http://music.163.com/weapi/v1/resource/comments?id=R_SO_4_33469997').read()
# print urllib2.urlopen('http://music.163.com/api/song/detail?id=33469997&ids=[33469997]').read()

import requests
import json
import os
import base64
from Crypto.Cipher import AES
from pprint import pprint
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext


def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = int(text.encode('hex'), 16)**int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)


def createSecretKey(size):
    return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]

def saveComments(musicid):
	#http://music.163.com/weapi/v1/resource/comments/R_SO_4_32807847/?
	url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_'+musicid+'/?csrf_token='
	headers = {
	    'Cookie': 'appver=1.5.0.75771;',
	    'Referer': 'http://music.163.com/',
	    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36',
	    'Connection':'keep-alive'
	}
	text = {
	    'username': 'lalala',
	    'password': 'mimimi',
	    'rememberLogin': 'true'
	}
	modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
	nonce = '0CoJUm6Qyw8W8jud'
	pubKey = '010001'
	text = json.dumps(text)
	secKey = createSecretKey(16)
	encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
	encSecKey = rsaEncrypt(secKey, pubKey, modulus)
	data = {
	    'params': encText,
	    'encSecKey': encSecKey
	}
	try:
		req = requests.post(url, headers=headers, data=data)
		res =[]
		#pprint(req.json())
		cmmts = ''
		for content in req.json()['hotComments']:
		    cmmts += (content['user']['nickname'].encode('utf-8')+':'+content['content'].encode('utf-8'))+'\n'

		for content in req.json()['comments']:
		    cmmts += (content['user']['nickname'].encode('utf-8')+':'+content['content'].encode('utf-8'))+'\n'
		f = open('comment/'+musicid+'.txt','w')
		f.write(cmmts)
		f.close()
		print musicid,'comment done'
	except Exception,e:
		print 'save comment failed' + musicid
		print e


def saveLyrics(musicid,musicName='',artistName='',albumName=''):
	headers = {
	    'Cookie': 'appver=1.5.0.75771;',
	    'Referer': 'http://music.163.com/'
	}
	url = 'http://music.163.com/api/song/media?id='+musicid

	req = requests.post(url, headers=headers)
	if('lyric' in req.json().keys()):
		f = open('lrc/'+musicid+'.lrc','w')
		f.write('['+musicName+'\t'+artistName+'\t'+albumName+']\r\n')
		f.write(req.json()['lyric'].encode('utf-8'))
		f.close()
		print musicid,'lyric done'
	else:
		print musicid , 'no lyric'
 
print saveComments('33469996')


