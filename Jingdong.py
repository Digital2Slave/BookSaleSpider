#!/usr/local/bin/python 
#-*- encoding:utf-8 -*-

import urllib2
from urllib2 import urlopen
import requests
from lxml import etree
from kit import etreeFromUrl
from collections import OrderedDict
import socket, time

def requestsUrl(url):
    """ requests """
    if (url==None) or (url==""):
        raise ("url error")
    
    # requests
    try:
        req = requests.get(url)
    except requests.exceptions.InvalidSchema as e:
        return ''
    except requests.exceptions.ConnectionError as e:
        time.sleep(30)
        print url
        return requestsUrl(url)
    except requests.exceptions as e:
        return requestsUrl(url)

    # return
    if (req.status_code==200):
        return req.text
    elif (req.status_code==404):
        return ''
    else:
        return requestsUrl(url)


def checkListResult(src):
    """
        check xpath return list whether [] or not.
    """
    if (src==[]):
        return ''
    else:
        return src[0]


def JingdongBookParse(bookurl, booksdict):
    
    if (bookurl==''):
        return booksdict

    texturl = requestsUrl(bookurl)

    if (texturl==''):
        return booksdict
    else:
        tree = etree.HTML(texturl)

        sels = tree.xpath('//ul[@class="p-parameter-list"]/li')

        for i in xrange(0,len(sels),1):
            sel = sels[i]
            
            selstr1 = checkListResult(sel.xpath('text()'))
            selstr2 = checkListResult(sel.xpath('a/text()'))
            selstr  = ''
            if (selstr2 != ''):
                selstr = selstr1.strip() + selstr2.strip()
            else:
                selstr = selstr1.strip()

            if (selstr != '') and (u'：' in selstr):
                sellist = selstr.split(u'：')
                booksdict[sellist[0]] = sellist[1]
        
        return booksdict


def JingdongBookSale(date, url):

    booksdict = OrderedDict()
    books = []

    for i in xrange(1,6,1):
        
        #http://book.jd.com/booktop/0-0-0.html?category=1713-0-0-0-10006-1#comfort --> 5#comfort
        pageurl = url.replace('1#comfort',  str(i)+'#comfort') 
        
        page = urlopen(pageurl)
        texturl = page.read()
        tree    = etree.HTML(texturl)
        
        # handle all books from current page 
        sels =  tree.xpath('//ul[@class="clearfix"]/li')
       
        for sel in sels:
            
            #!< bookdict for each book
            bookdict = OrderedDict()
            
            rank = sel.xpath('div[@class="p-num"]/text()')                             # 书籍排名
            bookurl = sel.xpath('div[@class="p-img"]/a/@href')                         # 书籍网址
            
            imgurls  = sel.xpath('div[@class="p-img"]/a/img/@data-lazy-img')           # 书籍封面(small)
            strs     = checkListResult(imgurls)
            imgurl   = ''
            if ( strs != ''):
                imgurl = strs.replace('/n3/','/n0/')                                   # 书籍封面(big) 

            title   = sel.xpath('div[@class="p-detail"]/a/@title')                     # 书籍名称
            author  = sel.xpath('div[@class="p-detail"]/dl[1]/dd/a/text()')            # 作者
            
            # !< write book data to bookdict.
            bookdict['rank']  = checkListResult(rank)
            bookdict['title'] = checkListResult(title)
            bookdict['author']= checkListResult(author)

            # !< get book's other information
            bookdict = JingdongBookParse(checkListResult(bookurl), bookdict)
            
            bookdict['imgurl']= imgurl
            bookdict['bookurl'] = checkListResult(bookurl)

            #for (key, val) in bookdict.items():
            #    print key, val 
            #print '\n'
            books.append(bookdict)
        #break
    booksdict[date] = books
    
    return booksdict

if (__name__=='__main__'):

    yearurl  = "http://book.jd.com/booktop/0-0-0.html?category=1713-0-0-0-10006-1#comfort"
    monthurl = "http://book.jd.com/booktop/0-0-0.html?category=1713-0-0-0-1-1#comfort" 
    
    year = '2013'
    yearbooksdict = JingdongBookSale(year, yearurl)
    
    #month = '20151'
    #monthbooksdict = JingdongBookSale(month, monthurl)
    
    

