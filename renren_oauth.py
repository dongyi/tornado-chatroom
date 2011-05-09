#!//usr/bin/env python
#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import base64
import hashlib
import hmac
import time
import urllib

RENREN_APP_API_KEY = "cf1b8d51c7d249fab1cf31ce01e035c3"
RENREN_APP_SECRET_KEY = "11eaae86c9c8401e89682e4156d592d7"


RENREN_AUTHORIZATION_URI = "http://graph.renren.com/oauth/authorize"
RENREN_ACCESS_TOKEN_URI = "http://graph.renren.com/oauth/token"
RENREN_SESSION_KEY_URI = "http://graph.renren.com/renren_api/session_key"
RENREN_API_SERVER = "http://api.renren.com/restserver.do"


class renrenuser:
    def __init__(self,id,name,img):
        self.id = id
        self.name = name
        self.img = img

def hash_params(params,secrect_key):
    hasher = hashlib.md5("".join(["%s=%s"%(x,params[x]) for x in sorted(params.keys())]))
    hasher.update(secrect_key)
    return hasher.hexdigest()

class renren:
    RENREN_APP_API_KEY = "cf1b8d51c7d249fab1cf31ce01e035c3"
    RENREN_APP_SECRET_KEY = "11eaae86c9c8401e89682e4156d592d7"


    RENREN_AUTHORIZATION_URI = "http://graph.renren.com/oauth/authorize"
    RENREN_ACCESS_TOKEN_URI = "http://graph.renren.com/oauth/token"
    RENREN_SESSION_KEY_URI = "http://graph.renren.com/renren_api/session_key"
    RENREN_API_SERVER = "http://api.renren.com/restserver.do"
    def first(self,redirect,response_type='code'):
        params = {}
        params['client_id'] = self.RENREN_APP_API_KEY
        params['response_type'] = response_type
        params['redirect_uri'] = redirect
        params = urllib.urlencode(params)
        url = RENREN_AUTHORIZATION_URI+'?'+params
        return url

def first_c(client_id,redirect_uri,response_type='token'):
    params = {}
    params['client_id'] = client_id
    params['response_type'] = response_type
    params['redirect_uri'] = redirect_uri
    params = urllib.urlencode(params)
    #rs = urllib.urlopen(RENREN_AUTHORIZATION_URI, params)
    #print rs.getcode()
    #print dir(rs)
    print params
    print RENREN_AUTHORIZATION_URI
    url = RENREN_AUTHORIZATION_URI+'?'+params
    print 'url:',url
    return url





def main():
    first(RENREN_APP_API_KEY,'http://graph.renren.com/oauth/login_success.html')

    
if "__main__" == __name__:
    main()




