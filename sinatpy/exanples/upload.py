#!/usr/bin/python
#coding=gbk

'''
Created on Aug 2, 2010

@author: ting
'''

import unittest
from weibopy.auth import OAuthHandler, BasicAuthHandler
from weibopy.api import API
        
class Test(unittest.TestCase):
    
    consumer_key= ""
    consumer_secret =""
    
    def __init__(self):
            """ constructor """
    
    def getAtt(self, key):
        try:
            return self.obj.__getattribute__(key)
        except Exception, e:
            print e
            return ''
        
    def getAttValue(self, obj, key):
        try:
            return obj.__getattribute__(key)
        except Exception, e:
            print e
            return ''
        
    def auth(self):
        
        if len(self.consumer_key) == 0:
            print "Please set consumer_key！！！"
            return
        
        if len(self.consumer_key) == 0:
            print "Please set consumer_secret！！！"
            return
                
        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth_url = self.auth.get_authorization_url()
        print 'Please authorize: ' + auth_url
        verifier = raw_input('PIN: ').strip()
        self.auth.get_access_token(verifier)
        self.api = API(self.auth)
    
    def basicAuth(self, source, username, password):
        self.authType = 'basicauth'
        self.auth = BasicAuthHandler(username, password)
        self.api = API(self.auth,source=source)
        
    def setToken(self, token, tokenSecret):
        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.setToken(token, tokenSecret)
        self.api = API(self.auth)
        
    def setAccessToken(self, token, tokenSecret):
        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.setToken(token, tokenSecret)
        self.api = API(self.auth, source=self.consumer_key)
    
    def upload(self, filename, message):
        message = message.encode("utf-8")
        status = self.api.upload(filename, status=message, lat="30", long="110")    
        self.obj = status
        id = self.getAtt("id")
        text = self.getAtt("text")
        #geo = self.getAtt("geo")
        user = self.getAtt("user")
        self.obj = user
        profile_image_url  = self.getAtt("profile_image_url")
        
        #self.obj = geo
        #type     = self.getAtt("type")
        #coordinates  = self.getAtt("coordinates")
        print("upload,id="+ str(id) +",text="+ text +",profile_image_url="+ profile_image_url)

test = Test()
test.basicAuth('consumer_key', 'username', 'password')
#test.setToken("key", "secret")
test.upload("test.jpg", "=upload-test-测试")

