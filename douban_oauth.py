#!/usr/bin/env python
#coding:utf-8
import sys
reload(sys)
import urllib
import hashlib
import time
import urlparse
import httplib
import random
import base64
import hmac


sys.setdefaultencoding("utf-8")
def to_signature_key(method, url, data):
    keys = list(data.keys())
    keys.sort()
    encoded = urllib.quote("&".join([key+"="+data[key] for key in keys]))
    return "&".join([method, urllib.quote(url, safe="~"), encoded])




def request_token_params(consumer_key, consumer_secret, path, method='GET'):
    data={}
    data['oauth_consumer_key']=consumer_key
    data['oauth_signature_method']='HMAC-SHA1'
    data['oauth_timestamp']=str(int(time.time()))
    data['oauth_nonce']=''.join([str(random.randint(0,9)) for i in range(10)])
    print data

    msg = to_signature_key(method, path, data)
    print msg

    signed = base64.b64encode(hmac.new(consumer_secret+"&", msg, hashlib.sha1).digest())
    print signed
    data['oauth_signature']=signed
    return data

def result2dict(res):
    d = {}
    params = res.split('&')
    for p in params:
        d[p.split('=')[0]] = p.split('=')[1]
    return d

def access_token_params(consumer_key, consumer_secret, oauth_token, oauth_secret, path, method='GET'):
    data={}
    data['oauth_consumer_key']=consumer_key
    data['oauth_signature_method']='HMAC-SHA1'
    data['oauth_timestamp']=str(int(time.time()))
    data['oauth_nonce']=''.join([str(random.randint(0,9)) for i in range(10)])
    data['oauth_token'] = oauth_token 

    msg = to_signature_key(method, path, data)
 #   print msg

    signed = base64.b64encode(hmac.new(consumer_secret+"&"+oauth_secret, msg, hashlib.sha1).digest())
  #  print signed
    data['oauth_signature']=signed
    return data

def access_params(consumer_key, consumer_secret, access_token,access_token_secret, path, method='GET'):
    data={}
    data['oauth_consumer_key'] = consumer_key
    data['oauth_token'] = access_token
    data['oauth_signature_method'] = 'HMAC-SHA1'
    data['oauth_timestamp'] = str(int(time.time()))
    data['oauth_nonce']=''.join([str(random.randint(0,9)) for i in range(10)])
    msg = to_signature_key(method, path, data)
    signed = base64.b64encode(hmac.new(consumer_secret+"&"+access_token_secret, msg, hashlib.sha1).digest())
    data['oauth_signature'] = signed
    return data


class doubanoauth:
    consumer_key = "0f0b1d1ab36508da2d2157501a2f1a8e"
    consumer_secret = "1bd0072da311382e"
    access_token_path = "http://www.douban.com/service/auth/access_token"
    request_token = {}
    conn = httplib.HTTPConnection("www.douban.com", 80)
    def stepone(self, callback):
        # step-one
        request_token_path = "http://www.douban.com/service/auth/request_token"
        params = request_token_params(consumer_key="0f0b1d1ab36508da2d2157501a2f1a8e", consumer_secret="1bd0072da311382e", path="http://www.douban.com/service/auth/request_token")
        self.conn.request('GET', request_token_path+"?"+urllib.urlencode(params))
        res = self.conn.getresponse().read()
        self.request_token = result2dict(res) 
        return 'http://www.douban.com/service/auth/authorize?oauth_token=%s&oauth_callback=%s'%(self.request_token['oauth_token'], callback)

    def steptwo(self, token, secret):
        params = access_token_params(self.consumer_key,
                             self.consumer_secret,
                             token,
                             secret,
                             self.access_token_path)
        self.conn.request('GET', self.access_token_path+"?"+urllib.urlencode(params))
        res = self.conn.getresponse().read()
        access_token = result2dict(res)
        return access_token

    def oauth_header(self,consumer_key, consumer_secret, oauth_token, oauth_secret, path, realm):
        data = access_token_params(consumer_key, consumer_secret, oauth_token, oauth_secret, path, method="GET")
        header_string = ','.join([key+'="'+data[key]+'"' for key in data.keys()])
        return 'OAuth realm="'+realm+'",'+header_string

    def stepthree(self,token,secret,posturl='http://api.douban.com/people/45116439',id='45116439',body=None):

        content = """<?xml version='1.0' encoding='UTF-8'?>
        <entry xmlns:ns0="http://www.w3.org/2005/Atom" xmlns:db="http://www.douban.com/xmlns/">
        <content>真谛很牛逼的</content>
        </entry>
        """

        header = {}
        header['Authorization'] = self.oauth_header(self.consumer_key, self.consumer_secret,token, secret,posturl, "http://api.douban.com")
       # header['Content-Type'] = 'application/atom+xml'
        print header

        self.conn.request('GET', posturl,body, header)
        res = self.conn.getresponse().read()
        self.conn.close()
        url = txt_wrap_by('<link href="','" rel="alternate"/>',res)
        print url
        me = txt_wrap_by('<title>','</title>',res)
        print me
        image_url = txt_wrap_by('<link href="','" rel="icon"/>',res)
        print image_url
        item = douban_iterm(id,me,url,image_url)

        return item
class douban_iterm:
    def __init__(self,id,me,url,profile_image_url):
        self.id = id
        self.username = me
        self.url = url
        self.profile_image_url = profile_image_url

def txt_wrap_by(start_str, end, html):
        start = html.find(start_str)
        if start >= 0:
            start += len(start_str)
            end = html.find(end, start)
            if end >= 0:
                return html[start:end].strip()





def main():
    consumer_key = "0f0b1d1ab36508da2d2157501a2f1a8e"
    consumer_secret = "1bd0072da311382e"
    access_token_path = "http://www.douban.com/service/auth/access_token"
    # step-one
    conn = httplib.HTTPConnection("www.douban.com", 80)
    request_token_path = "http://www.douban.com/service/auth/request_token"
    params = request_token_params(consumer_key="0f0b1d1ab36508da2d2157501a2f1a8e", consumer_secret="1bd0072da311382e", path="http://www.douban.com/service/auth/request_token")
    conn.request('GET', request_token_path+"?"+urllib.urlencode(params))
    res = conn.getresponse().read()
    print res
    request_token = result2dict(res) 
    print 'http://www.douban.com/service/auth/authorize?oauth_token=%s'%request_token['oauth_token']
    s = raw_input("have u ?")
    # step-two
    params = access_token_params(consumer_key,
                             consumer_secret,
                             request_token['oauth_token'],
                             request_token['oauth_token_secret'],
                             access_token_path)
    conn.request('GET', access_token_path+"?"+urllib.urlencode(params))
    res = conn.getresponse().read()
    print res
    access_token = result2dict(res)
    print access_token
    access_path = raw_input("input url!!!")
    params_access = access_params(consumer_key, consumer_secret, access_token['oauth_token'],access_token['oauth_token_secret'], access_path, method='GET')
    conn.request('GET', access_path+"?"+urllib.urlencode(params_access))
    res_access = conn.getresponse().read()
    print res_access





if "__main__" == __name__:
    main()

