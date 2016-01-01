#!/usr/bin/env python2
#coding=utf8
import sys, os
import jcc
import lucene
import threading, time
import urlparse
import codecs
import sys
import time
reload(sys)
sys.setdefaultencoding("utf-8")

from bs4 import BeautifulSoup
from datetime import datetime


# from java.io import File
# from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
# from org.apache.lucene.analysis.standard import StandardAnalyzer
# from org.apache.lucene.analysis.core import WhitespaceAnalyzer

# from org.apache.lucene.document import Document, Field, FieldType
# from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
# from org.apache.lucene.store import SimpleFSDirectory
# from org.apache.lucene.util import Version


from lucene import QueryParser,\
                   IndexSearcher,\
                   WhitespaceAnalyzer,IndexWriter,\
                   SimpleFSDirectory,\
                   File, VERSION,\
                   initVM, Version,Document,Field,\
                   BooleanQuery,\
                   BooleanClause,LimitTokenCountAnalyzer,IndexWriterConfig,\
                   Term, WildcardQuery



"""
This class is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""

class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)
        store = SimpleFSDirectory(File(storeDir))

        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)

        writer = IndexWriter(store, config)

        self.indexDocs(writer)
        ticker = Ticker()
        print(  'optimizing index' ),
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print(  'done' )

    def indexDocs(self, writer):

        f = codecs.open('index.txt','r',encoding='utf-8')
        files = set()
        for line in f.xreadlines():
            ls = line.split()
            files.add(ls[0][:-5])
        f.close()

        for item in files:

            basic_info = 'basic_info/' + item + '.txt'
            if(not os.path.exists(basic_info)):
                continue
            lrc_jieba = 'lrc_jieba/' + item + '.txt'
            url = 'http://music.163.com/song?id=' + item

            #处理基本信息

            f = codecs.open(basic_info,'r',encoding='utf-8')
            lines =  list(f.xreadlines())
            if(len(lines)!=4):
                continue
            music_name = lines[0]
            artist = lines[1]
            album_name = lines[2]
            description = lines[3]
            if(description=='no description'):
                description = ' '
            f.close()
            lrc = ' '
            if(os.path.exists(lrc_jieba)):
                #记录分好词的歌词
                f = codecs.open(lrc_jieba,'r',encoding='utf-8')
                lrc = f.read()
                f.close()

            import jieba
            music_name_2 = ' '.join(jieba.cut(music_name))
            contentToIndex = music_name_2*50 + ' ' + artist + ' ' + album_name + ' ' + description + ' ' + lrc + ' '

            doc = Document()
            doc.add(Field("musicID", item ,
                                 Field.Store.YES,
                                 Field.Index.NOT_ANALYZED))


            doc.add(Field('music_name', music_name,
                                 Field.Store.YES,
                                 Field.Index.NOT_ANALYZED))

            doc.add(Field("url", url,
                                 Field.Store.YES,
                                 Field.Index.NOT_ANALYZED))

            doc.add(Field("artist", artist ,
                                 Field.Store.YES,
                                 Field.Index.NOT_ANALYZED))
            doc.add(Field("album_name", album_name ,
                                 Field.Store.YES,
                                 Field.Index.NOT_ANALYZED)) 
            
            #进行索引的两项
            doc.add(Field("lrc", lrc,
                                 Field.Store.YES,
                                 Field.Index.ANALYZED))

            doc.add(Field("content", contentToIndex,
                                 Field.Store.YES,
                                 Field.Index.ANALYZED))
            
            writer.addDocument(doc)
            print item , 'ok'
  
if __name__ == '__main__':
    #lucene.initVM() #
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    IndexFiles("indexFORsongs", WhitespaceAnalyzer(Version.LUCENE_CURRENT))
    end = datetime.now()
    print end - start
