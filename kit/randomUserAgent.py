#!~/.virtualenvs/cv/bin/python 
#-*- encoding:utf-8 -*-
import sys 
reload(sys) 
sys.setdefaultencoding('utf-8') #'utf8'

import random, json

def getRandomUseragent(user_agent_file=None):
    """
    To get a random User_agent from user_agent_file or not.
    the default user_agent_list composes chrome,IE,firefox,Mozilla,opera,netscape
    for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
    """
    
    if (user_agent_file != None):
        #http://www.useragentstring.com/pages/useragentstring.php
        browerfile = file(user_agent_file, 'rb')
        browerdata = json.load(browerfile)
        browerfile.close()

        PCbrower = browerdata['brower']      #9502
        MBbrower = browerdata['mobilebrower']#512
        user_agent_list = PCbrower
        #print len(PCbrower), PCbrower[0]
        #print len(MBbrower), MBbrower[0]
    else:
	user_agent_list = [
        'Mozilla/40.0.3 (Macintosh; Intel Mac OS X 10_10_4)',\
        'AppleWebKit/536.5 (KHTML, like Gecko)',\
        'Chrome/19.0.1084.54 Safari/536.5',\
        \
        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31',\
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17',\
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',\
        \
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',\
        'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',\
        'Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',\
        \
        'Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',\
        'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1',\
        'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:15.0) Gecko/20120910144328 Firefox/15.0.2',\
        \
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',\
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a3pre) Gecko/20070330',\
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.13; ) Gecko/20101203',\
        \
        'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',\
        'Opera/9.80 (X11; Linux x86_64; U; fr) Presto/2.9.168 Version/11.50',\
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; de) Presto/2.9.168 Version/11.52',\
        \
        'Mozilla/5.0 (Windows; U; Win 9x 4.90; SG; rv:1.9.2.4) Gecko/20101104 Netscape/9.1.0285',\
        'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.8.1.7pre) Gecko/20070815 Firefox/2.0.0.6 Navigator/9.0b3',\
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',\
    ]

    return random.choice(user_agent_list)

if (__name__=='__main__'):

    user_agent_file = './UserAgentString.json'

    User_agent = getRandomUseragent(user_agent_file)

    print 'random choice User_agent --> ', User_agent
