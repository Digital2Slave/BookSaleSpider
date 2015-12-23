#!~/.virtualenvs/cv/bin/python 
#-*- encoding:utf-8 -*-
import sys 
reload(sys) 
sys.setdefaultencoding('utf-8') #'utf8'

import re, base64, random

def getRandomProxy(proxy_file=None):
    """
    To get a random proxy proxy_file.
    # proxy_file containing entries like
    # http://host1:port
    # !http://username:password@host2:port
    # http://host3:port
    # ...
    """
    
    if (proxy_file != None):
        
        f = open(proxy_file, 'rb')
        
        proxy_list = []
        
        for line in f.readlines():
           
            if not line.startswith('http'):
                line = 'http://' + line 
            
            ele = line.strip()
            proxy_list.append(ele)

        f.close()
        
        return random.choice(proxy_list)

if (__name__=='__main__'):
    
    proxy_file = './proxy_list.txt'

    print 'random.choice proxy --> ',  getRandomProxy(proxy_file)
