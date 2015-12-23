#!/usr/local/bin/python  
#-*- encoding:utf-8 -*-
import sys 
reload(sys) 
sys.setdefaultencoding('utf-8') #'utf8'

import os,re 

from urllib2 import Request, urlopen, URLError
from lxml import etree
from collections import OrderedDict
from kit import etreeFromUrl

def AmazonBookParse(bookurl, orderdict):
    """
    Amazon Book Parse. 单独处理每一本书籍信息
    """
    sel, urlbody = etreeFromUrl.getEtreeFromUrl(bookurl)
    
    # 书名 book OR kindle
    name = ''
    bookname = sel.xpath('//span[@id="productTitle"]/text()')
    kindlename = sel.xpath('//h1[@class="parseasinTitle"]/span/span/text()')
    if (bookname != None) and (bookname != []):
        name = bookname[0]
    elif (kindlename != None and (kindlename != [])):
        name = kindlename[0]
    orderdict['书名'] = name.strip()

    # 作者 author of book OR author of kindle
    author = sel.xpath('//span[@class="author notFaded"]/a[@class="a-link-normal"]/text()')
    authorlocation = sel.xpath('//span[@class="author notFaded"]/span/span[@class="a-color-secondary"]/text()')
    authors = ''
    for i in range(len(author)):
        name0 = author[i]+authorlocation[i]
        authors += name0

    if (authors == ''):
        kindleauthor         = sel.xpath('//div[@class="buying"]/span/a/text()')
        kindlelocationauthor = sel.xpath('//div[@class="buying"]/span/text()')
        kindlelocation = ''
        if (kindlelocationauthor != None) and (kindlelocationauthor != []):
            kindlelocation = kindlelocationauthor[1].strip()
        for i in range(len(kindleauthor)):
            name1 = kindleauthor[i] + kindlelocation[i]
            authors += name1
    orderdict['作者'] = authors

    #!< 书籍其它信息(不包括用户评分，亚马逊热销商品排名，书籍封面URL) book OR kindle
    detailNameTmp = sel.xpath('//div[@class="content"]/ul/li/b/text()')
    detailName = [i.strip('\n :') for i in detailNameTmp]
    Name = detailName[:-2]

    detailValueTmp = sel.xpath('//div[@class="content"]/ul/li/text() | //div[@class="content"]/ul/li/a/text()')
    detailValue = []
    for vt in detailValueTmp:
        vt = vt.strip('\n >')
        if (vt != '') and (vt != u'\xa0'):
            detailValue.append(vt)
    Value = detailValue[:len(Name)]

    Num = len(Name)
    for i in xrange(Num):
        key = Name[i]
        val = Value[i]
        if (':' in key):
            key = key.strip(':')
        if (':' in val):
            val = val.strip(':')
        val = val.strip(' ')
        orderdict[key] = val
    #!< kindle
    try:
        xray = sel.xpath('//a[@id="xrayPop"]/span/text()')
        orderdict['xRay'] = xray[0]
    except:
        orderdict['xRay'] = None

    #!< 用户评分，亚马逊热销商品排名 book OR kindle
    score = ''
    try:
        #score = sel.xpath('//span[@id="acrPopover"]/@title')
        score = sel.xpath('//div[@id="avgRating"]/span/text()')
        if (score != []):
            score = score[0].strip()
        else: # kindle
            score = sel.xpath('//div[@class="gry txtnormal acrRating"]/text()')
            if (score != []):
                score = score[0].strip()
    except:
        score = None

    rank =''
    try: # book and kindle
        ranks = sel.xpath('//li[@id="SalesRank"]/text()')
        if (ranks != []) and (len(ranks)>=2):
            for i in ranks[1]:
                if (' ' not in i) and ('\n' not in i) and ('(' not in i):
                    rank += i
    except:
        rank = None
    orderdict['用户评分'] = score
    orderdict['亚马逊热销商品排名'] = rank

    #!< 书籍价格 book OR kindle
    PZprice = sel.xpath('//span[@class="a-button-inner"]/a/span/span/text()')
    if (PZprice != []): # book
        if(len(PZprice)==1):
            price = PZprice[0].strip()
            orderdict['平装'] = price
        else:
            price = [s.strip() for s in PZprice]
            orderdict['精装'] = price[0]
            orderdict['平装'] = price[1]
    else:
        PZprice = sel.xpath('//b[@class="priceLarge"]/text()')
        if (PZprice != []):
            price = PZprice[0].strip()
            orderdict['Kindle电子书价格'] = price

    #!< 书籍封面URL coverurl of book OR coverurl of kindle
    #1.books
    texturl = urlbody
    #Re = r"http://ec4.images-amazon.com/images/I/[\w]+-?%?_?.?[\w]+.jpg"
    Re = r'''"mainUrl":"http://ec4.images-amazon.com/images/I/[\w]+.+[\w]+.jpg"'''
    imgurls = re.findall(Re, texturl)

    #2.kindle books
    kindleRe = r'''"large":"http://ec4.images-amazon.com/images/I/[\w]+.+[\w]+.jpg"'''
    kimgurls = re.findall(kindleRe, texturl)

    imgurl = str()
    if (imgurls != []):# be sure mainUrl in imgurls
        #imgurl = imgurls[0]
        endindex = imgurls[0].find('''","dimensions"''')
        imgurl = imgurls[0][11:endindex]

    elif(kimgurls != []):# be sure large in imgurls
        endindex = kimgurls[0].find('''","variant"''')
        imgurl = kimgurls[0][9:endindex]
    else:
        print ("Not cover!")

    #!< write book cover to dest_path
    if (imgurl.startswith('http://ec4.images-amazon.com/images/I/')):
        # coverurls eg: 'http://ec8.images-amazon.com/images/I/91bpj-PbL1L.jpg'
        orderdict['imgurl'] = imgurl
    else:
        orderdict['imgurl'] = None

    return orderdict

def AmazonYearBookSale(year, url):
    """
    Amazon Year Book Sale. 2010-->2015(half)
    """
    sel, urlbody = etreeFromUrl.getEtreeFromUrl(url)
    bookurls = sel.xpath('//div[@class="inner"]/div/a/@href')
   
    bookdicts = OrderedDict()
    books = []
    if bookurls:
        for l in bookurls:
            bookurl = str()
            if (not l.startswith('http://www.amazon.cn')):
                bookurl = 'http://www.amazon.cn'+l
            else:
                bookurl = l
            orderdict = OrderedDict()
            bookdict = AmazonBookParse(bookurl, orderdict) 
            #print bookdict
            books.append(bookdict)
    bookdicts[year] = books

    return bookdicts

def RecursiveForNextpage(sel,monthbooks):
    # nextpage
    nextpage = sel.xpath('//a[@class="pagnNext"]/@href')
    if nextpage:
        nexturl = 'http://www.amazon.cn' + nextpage[0]
        nextsel,nextbody = etreeFromUrl.getEtreeFromUrl(nexturl)
        RecursiveForNextpage(nextsel,monthbooks)

    # books
    bookurls = sel.xpath('//div[@class="a-row a-spacing-small"]/a/@href')
    if bookurls:
        for l in bookurls:
            bookdict = OrderedDict()
            bookurl = str()
            if (not l.startswith('http://www.amazon.cn')):
                bookurl = 'http://wwww.amazon.cn' + l
            else:
                bookurl = l
            bookdict = AmazonBookParse(bookurl,bookdict)
            monthbooks.append(bookdict)
        return monthbooks

def AmazonMonthBookSale(url):
    """
    Amazon Month BookSales.
    """
    sel, urlbody = etreeFromUrl.getEtreeFromUrl(url)
    months = sel.xpath('//div[@class="left_nav browseBox"]/ul/li/a/@href')
    
    if months:
        """
        monthYear like {
            '2014':[
            {'20141':[ {book0},{book1}...]}, 
            {'20142':[ {book0},{book1}...]}, 
            {'20143':[ {book0},{book1}...]}, 
                ...],

            '2015':[...]
        }
        """
        monthYearbook = OrderedDict()
        monthYeardata = []

        cnt = 0
        for l in months[::-1]:
            
            # month number
            cnt +=1
            yearmonth = cnt%12 
            if (yearmonth==0):
                yearmonth = 12
            
            # monthurl
            monthurl = str()
            if (not monthurl.startswith('http://www.amazon.cn')):
                monthurl = 'http://www.amazon.cn' + l
            else:
                monthurl = l
            
            # month books
            monthbookdicts = OrderedDict()
            monthbooks = []
            
            if (cnt <= 12):
                # 2014
                monthsel, monthbody = etreeFromUrl.getEtreeFromUrl(monthurl)
                monthbooks = RecursiveForNextpage(monthsel, monthbooks) 
                monthbookdicts['2014'+str(yearmonth)] = monthbooks
                monthYeardata.append(monthbookdicts)
                #print '201401 books number --> ', len(monthbooks)
                #print '201401 books example -->', monthbooks[0]
            else:
                # 2015
                monthsel, monthbody = etreeFromUrl.getEtreeFromUrl(monthurl)
                monthbooks = RecursiveForNextpage(monthsel, monthbooks) 
                monthbookdicts['2015'+str(yearmonth)] = monthbooks
                monthYeardata.append(monthbookdicts)
                #print '201501 books number --> ', len(monthbooks)
                #print '201501 books example -->', monthbooks[0]
        
        monthYearbook['2014'] = monthYeardata[:12]
        monthYearbook['2015'] = monthYeardata[12:]
        return monthYearbook


if (__name__=='__main__'):

    starts_month_urls = [
    "http://www.amazon.cn/b/ref=amb_link_30652892_2?ie=UTF8&node=1559222071&pf_rd_m=A1AJ19PSB66TGU&pf_rd_s=merchandised-search-1&pf_rd_r=1RZ4QVKKCE5AESFRJDX3&pf_rd_t=101&pf_rd_p=260687732&pf_rd_i=658390051",
    ]

    starts_year_urls = [
			"2010http://www.amazon.cn/gp/feature.html/ref=amb_link_97634752_4?ie=UTF8&docId=45988&pf_rd_m=A1AJ19PSB66TGU&pf_rd_s=merchandised-search-left-2&pf_rd_r=1HKH38AW6K7VQMJR2ZMY&pf_rd_t=101&pf_rd_p=242750372&pf_rd_i=1457350071",
    ]

    '''
    for yearUrl in starts_year_urls:
	year = yearUrl[:4]
	url  = yearUrl[4:]
        bookdicts = AmazonYearBookSale(year, url)
        print bookdicts
        break
    '''
    monthYearbook = OrderedDict()
    for m in starts_month_urls:
        monthYearbook = AmazonMonthBookSale(m)
        #break
