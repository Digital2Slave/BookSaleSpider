#!~/.virtualenvs/cv/bin/python
#-*- encoding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #'utf8'

import socket, time, requests

import urllib2
from urllib2 import Request, urlopen, URLError, HTTPError

import randomProxy, randomUserAgent
from lxml import etree
# BeautifulSoup抓取网页中的中文乱码
import bs4

def requestsUrl(url):
    """ requests """
    if (url==None) or (url==""):
        raise ("url error")

    # requests
    try:
        req = requests.get(url)
    except requests.RequestException as e:
        return requestsUrl(url)
    except requests.exceptions as e:
        return requestsUrl(url)

    # return
    if (req.status_code==200):
        return req.text
    else:
        return requestsUrl(url)


def urllib2Url(url):
    """ urllib2 """
    if (url==None) or (url==""):
        raise ("url error")

    # Set Proxy
    enable_proxy = False
    Proxy  = randomProxy.getRandomProxy('./proxy_list.txt')
    proxy_handler = urllib2.ProxyHandler({"http":Proxy})
    null_proxy_handler = urllib2.ProxyHandler({})
    if enable_proxy:
        opener = urllib2.build_opener(proxy_handler)
    else:
        opener = urllib2.build_opener(null_proxy_handler)

    # Set User_agent
    User_agent = randomUserAgent.getRandomUseragent(None)
    headers    = {'Use-Agent':User_agent}
    req        = Request(url, headers=headers)

    # Check open function
    try:
        response = opener.open(req)
    except urllib2.URLError, e:
        #print e.reason, url
        return urllib2Url(url)
    except urllib2.HTTPError, e:
        #print e.code, url
        return urllib2Url(url)

    # Return
    if (response.getcode()==200):
        return response.read()
    else:
        return urllib2Url(url)


def getEtreeFromUrl(url):
    """
    To get Selector-like from URL.
    """

    # 测试中文乱码
    #page = bs4.BeautifulSoup(page, from_encoding='GB18030')

    try:
        page = requestsUrl(url)
    except:
        page = urllib2Url(url)

    sel = etree.HTML(page)

    return sel, page


if (__name__=='__main__'):

    url = 'http://www.baidu.com'

    sel,page = getEtreeFromUrl(url)

    print sel.xpath('//a/@href')
