#coding=utf-8
import web
from web import form
import urllib2
import os
import SearchMusic
import tools
from datetime import datetime


urls= (
    '/','index',
    '/s','s'
)

render = web.template.render('templates')

class index:
    def GET(self):
        return render.formtest()
 
class s:
    def GET(self):

        global old_keyword,old_res_list
        user_data= web.input() 
        
        if(SearchMusic.vm_env==None):
            SearchMusic.init()
        
        SearchMusic.vm_env.attachCurrentThread() 

        keyword = user_data['keyword']
        typ = 0 # 0 is text and 1 is image
        if(user_data.has_key('typ')):
            typ = 0 + (user_data['typ']=='Search Images')
        nocrct = False
        print typ
        p = 1
        if(user_data.has_key('p')):
            p = int(user_data['p'])
        if(keyword=='' or keyword==None):
            return render.formtest()
        if(typ==0):
            havecrct = False
            oriKW = keyword
            relevList = []
            crctKW,relevList = tools.checkFuzz(keyword)
            havecrct = not (crctKW==oriKW)
            res_list,total = SearchMusic.run(oriKW,p,8)

            return render.result(keyword,res_list,p,8,total,crctKW,havecrct,relevList)
        else:
            #res_list,total = SearchImages_webVersion.run(keyword,p,60)
            return render.img_res(keyword,res_list,p,60,total)


if __name__ == "__main__":
    SearchMusic.init()
    #SearchImages_webVersion.init()
    app = web.application(urls, globals())
    app.run()