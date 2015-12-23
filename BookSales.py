#!~/.virtualenvs/cv/bin/python
#-*- encoding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #'utf8'

import json
import pymongo
from pymongo import MongoClient
from collections import OrderedDict

import Amazon, Dangdang, Jingdong


def AmazonToMongoDB(YearCollection, MonthCollection):
    """
    Amazon BookSale.
    """
    # Amazon Year Month BookSale.
    starts_month_urls = [
            "http://www.amazon.cn/b/ref=amb_link_30652892_2?ie=UTF8&node=1559222071&pf_rd_m=A1AJ19PSB66TGU&pf_rd_s=\
            merchandised-search-1&pf_rd_r=1RZ4QVKKCE5AESFRJDX3&pf_rd_t=101&pf_rd_p=260687732&pf_rd_i=658390051"
    ]

    #60, 129, 147, 180, 200, 160
    starts_year_urls = [
	                "2010http://www.amazon.cn/gp/feature.html/ref=amb_link_97634752_4?ie=UTF8&docId=45988&pf_rd_m=A1AJ19PSB66TGU&pf_rd_s=\
			merchandised-search-left-2&pf_rd_r=1HKH38AW6K7VQMJR2ZMY&pf_rd_t=101&pf_rd_p=242750372&pf_rd_i=1457350071",

			"2011http://www.amazon.cn/gp/feature.html/ref=amb_link_97634752_3?ie=UTF8&docId=97198&pf_rd_m=A1AJ19PSB66TGU&pf_rd_s=\
			merchandised-search-left-2&pf_rd_r=1HKH38AW6K7VQMJR2ZMY&pf_rd_t=101&pf_rd_p=242750372&pf_rd_i=1457350071",

			"2012http://www.amazon.cn/gp/feature.html/ref=amb_link_31790272_1?ie=UTF8&docId=180128&pf_rd_m=A1AJ19PSB66TGU&pf_rd_s=\
			foil-top&pf_rd_r=1HBBWGRQTAVDH3401S6G&pf_rd_t=1401&pf_rd_p=66915512&pf_rd_i=181758",

			"2013http://www.amazon.cn/gp/feature.html/ref=amb_link_97634752_1?ie=UTF8&docId=816848&pf_rd_m=A1AJ19PSB66TGU&pf_rd_s=\
			merchandised-search-left-2&pf_rd_r=1VJDQ4K7DCQ7XY43S4QE&pf_rd_t=101&pf_rd_p=242750372&pf_rd_i=1457350071",

			"2014http://www.amazon.cn/b/ref=amb_link_97647152_1?ie=UTF8&node=1457350071&pf_rd_m=A1AJ19PSB66TGU&pf_rd_s=\
			foil-top&pf_rd_r=1TR7F6D79EJQANMBVW61&pf_rd_t=1401&pf_rd_p=251541212&pf_rd_i=1525068",

			"2015http://www.amazon.cn/b/ref=amb_link_100002232_14?ie=UTF8&node=1489090071&pf_rd_m=A1AJ19PSB66TGU&pf_rd_s=\
			merchandised-search-leftnav&pf_rd_r=0D1VGF7QZ9EB77CR1MZR&pf_rd_t=101&pf_rd_p=256328612&pf_rd_i=658390051"
    ]

    #
    for yearUrl in starts_year_urls:
	year = yearUrl[:4]
	url  = yearUrl[4:]
        bookdicts = Amazon.AmazonYearBookSale(year,url)
        YearCollection.insert(bookdicts)

    for m in starts_month_urls:
        bookdicts = Amazon.AmazonMonthBookSale(m)
        MonthCollection.insert(bookdicts)


def DangdangToMongoDB(YearCollection, MonthCollection):
    """
    Dangdang BookSale.
    """
    # Year BookSale
    starts_year_urls  = [
                            "http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-year-2011-0-1-1", # 25
                            "http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-year-2012-0-1-1", # 25
                            "http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-year-2013-0-1-1", # 25
                            "http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-year-2014-0-1-1"  # 25
                        ]

    starts_month_urls = [
                            "http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-month-2015-1-1-1" # 25 for every month
                        ]

    for yearUrl in starts_year_urls:
        year = yearUrl[-10:-6]
        bookdicts = Dangdang.DangdangBookSale(year, yearUrl)
        YearCollection.insert(bookdicts)
    print 'Year ok!'

    for i in xrange(1,11,1):
        month = '2015-' + str(i)
        monthurl = starts_month_urls[0].replace('2015-1',month)
        bookdicts = Dangdang.DangdangBookSale(month,monthurl)
        MonthCollection.insert(bookdicts)
        print month + 'Done!'
    print 'Month ok!'



def JingdongToMongoDB(YearCollection, MonthCollection):
    """
    Jingdong BookSale.
    """

    # Year BookSale
    starts_year_urls = [
            "http://book.jd.com/booktop/0-0-0.html?category=1713-0-0-0-10006-1#comfort", # 2013
            "http://book.jd.com/booktop/0-0-0.html?category=1713-0-0-0-10005-1#comfort"  # 2014
        ]

    # Month BookSale
    starts_month_urls = [
            "http://book.jd.com/booktop/0-0-0.html?category=1713-0-0-0-1-1#comfort" # "http://book.jd.com/booktop/0-0-0.html?category=1713-0-0-0-2-1#comfort"
        ]

    years = ["2013", "2014"]
    for i in xrange(len(years)):
        year = years[i]
        yearUrl = starts_year_urls[i]
        bookdicts = Jingdong.JingdongBookSale(year, yearUrl)
        YearCollection.insert(bookdicts)
    print 'Year ok!'

    for i in xrange(1,11,1):
        month = '2015-' + str(i)
        monthurl = starts_month_urls[0].replace('1-1',str(i)+'-1')
        bookdicts = Jingdong.JingdongBookSale(month, monthurl)
        MonthCollection.insert(bookdicts)
        print month + 'Done!'
    print 'Month ok!'


def run(function, YearCollection, MonthCollection):

    function(YearCollection, MonthCollection)

    print "Done!"


if (__name__=='__main__'):

    # MongoDB connection
    MONGODB_SERVER = 'localhost'
    MONGODB_PORT = 27017
    connection = pymongo.MongoClient(MONGODB_SERVER, MONGODB_PORT)

    # MongoDB db
    MONGODB_DB = 'BookSale'
    db         = connection[MONGODB_DB]

    # MongoDB collection
    YearCollection1  = db['Amazon']
    MonthCollection1 = db['AmazonMonth']
    run(AmazonToMongoDB, YearCollection1, MonthCollection1)

    YearCollection2  = db['DangdangYear']
    MonthCollection2 = db['DangdangMonth']
    run(DangdangToMongoDB, YearCollection2, MonthCollection2)

    YearCollection3   = db['JingdongYear']
    MonthCollection3  = db['JingdongMonth']
    run(JingdongToMongoDB, YearCollection3, MonthCollection3)
