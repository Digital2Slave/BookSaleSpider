#!/usr/local/bin/python
#-*- encoding:utf-8 -*-

import urllib2
from urllib2 import urlopen
import requests
from lxml import etree
from kit import etreeFromUrl
from collections import OrderedDict
import socket, time
"""

rule:
small imgurl = 'http://img34.ddimg.cn/24/29/9213954-1_l.jpg'
big   imgurl = 'http://img34.ddimg.cn/24/29/9213954-1_u_1.jpg'

"""

def requestsUrl(url):
    """ requests """
    if (url==None) or (url==""):
        raise ("url error")

    # requests
    try:
        req = requests.get(url)
    except requests.exceptions.InvalidSchema as e:
        return None
    except requests.exceptions.ConnectionError as e:
        time.sleep(30)
        print url
        return requestsUrl(url)
    except requests.exceptions as e:
        return requestsUrl(url)

    #req = requests.get(url)
    # return
    if (req.status_code==200):
        return req.text
    elif (req.status_code==404):
        return None
    else:
        return requestsUrl(url)


def DangdangBookParse(bookurl):

    texturl = requestsUrl(bookurl)

    if (texturl==None):
        return ['', '']
    else:
        # !< get isbn
        isbn = ''
        tree = etree.HTML(texturl)
        isbns = tree.xpath('//div[@class="pro_content"]/ul/li[10]/text()')
        if (isbns!=[]):
            isbn = str(isbns[0][11:])

        # !< get classify
        classify1 = tree.xpath('//li[@class="clearfix fenlei"]/span[1]/a/text()')
        classify2 = tree.xpath('//li[@class="clearfix fenlei"]/span[2]/a/text()')
        classify3 = tree.xpath('//li[@class="clearfix fenlei"]/span[3]/a/text()')
        s1, s2, s3 = '', '', ''
        if (classify1 != []):
            for s in classify1:
                s = s + '>'
                s1 += s
        if (classify2 != []):
            for s in classify2:
                s = s + '>'
                s2 += s
        if (classify3 != []):
            for s in classify3:
                s = s + '>'
                s3 += s

        # return
        if (classify3 != []):
            return [isbn, s1, s2, s3]
        elif(classify2 != []):
            return [isbn, s1, s2]
        else:
            return [isbn, s1]



def checkListResult(src):
    """
        check xpath return list whether [] or not.
    """
    if (src==[]):
        return ''
    else:
        return src[0]


def DangdangBookSale(date, url):

    booksdict = OrderedDict()
    books = []

    for i in xrange(1,26,1):
        pageurl = url[:-1] + str(i)
        tree, pagetext = etreeFromUrl.getEtreeFromUrl(pageurl)

        #single book url. Note that: bookurl may not useful.
        sels =  tree.xpath('//ul[@class="bang_list clearfix bang_list_mode"]/li')

        for sel in sels:

            bookdict = OrderedDict()

            bookurl = sel.xpath('div[@class="pic"]/a/@href')                           # 书籍网址

            imgurls  = sel.xpath('div[@class="pic"]/a/img/@src')                       # 书籍封面(small)
            strs     = checkListResult(imgurls)
            imgurl   = ''
            if ( strs != ''):
                imgurl = strs[:-5] + 'u_1.jpg'                                         # 书籍封面(big)

            title   = sel.xpath('div[@class="name"]/a/text()')                         # 书籍名称

            star1   = sel.xpath('div[@class="star"]/a/text()')                         # 评论条数目
            star2   = sel.xpath('div[@class="star"]/span/text()')                      # 百分比推荐

            author  = sel.xpath('div[@class="publisher_info"]/a[1]/@title')            # 作者

            pubdate = sel.xpath('div[@class="publisher_info"]/span/text()')            # 出版日期
            puber   = sel.xpath('div[@class="publisher_info"]/a/text()')               # 出版社

            price   = sel.xpath('div[@class="price"]/p/span/text()')                   # 价格
            price_e = sel.xpath('div[@class="price"]/p[@class="price_e"]/span/text()') # 电子书价格

            # !< get ISBN for each book. isbn str, classify strs
            isbnclassify = DangdangBookParse(checkListResult(bookurl))
            isbn, classify = isbnclassify[0], isbnclassify[1:]
            bookdict['isbn']    = isbn
            bookdict['title']   = checkListResult(title)
            bookdict['star']    = checkListResult(star1) + checkListResult(star2)
            bookdict['author']  = checkListResult(author)
            bookdict['pubdate'] = checkListResult(pubdate)
            bookdict['puber']   = checkListResult(puber)
            bookdict['price']   = checkListResult(price)
            bookdict['price_e'] = checkListResult(price_e)
            bookdict['classify']= classify
            bookdict['imgurl']  = imgurl
            bookdict['bookurl'] = checkListResult(bookurl)

            #for (key, val) in bookdict.items():
            #    print key, val
            #print '\n'
            books.append(bookdict)

    booksdict[date] = books

    return booksdict



if (__name__=='__main__'):

    yearurl = "http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-year-2011-0-1-1"
    monthurl = "http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-month-2015-1-1-1"

    year = yearurl[-10:-6]
    yearbooksdict = DangdangBookSale(year, yearurl)
    #print yearbooksdict
    #print len(yearbooksdict[year])


