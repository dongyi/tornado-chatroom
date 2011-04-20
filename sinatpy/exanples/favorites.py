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
        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth_url = self.auth.get_authorization_url()
        print 'Please authorize: ' + auth_url
        verifier = raw_input('PIN: ').strip()
        self.auth.get_access_token(verifier)
        self.api = API(self.auth)
    def basicAuth(self, source, username, password):
        self.auth = BasicAuthHandler(username, password)
        self.api = API(self.auth,source=source)
        
    def setToken(self, token, tokenSecret):
        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.setToken(token, tokenSecret)
        self.api = API(self.auth)
        
    def favorites(self):
        statuses = self.api.favorites(id=1773365880)
        for status in statuses:
            self.obj = status
            sid = self.getAtt("id")
            text = self.getAtt("text")
            print "favorites---"+ str(sid) +":"+ text
        
    def create_favorite(self, id):
        status = self.api.create_favorite(id)
        self.obj = status
        sid = self.getAtt("id")
        text = self.getAtt("text")
        print "create_favorite---"+ str(sid) +":"+ text
            
    def destroy_favorite(self, id):
        msg = self.api.destroy_favorite(id)
        self.obj = msg
        mid = self.getAtt("id")
        text = self.getAtt("text")
        print "destroy_favorite---"+ str(mid) +":"+ text

test = Test()
#AccessToken的 key和Secret
test.setToken("key", "secret")
test.favorites()
#test.create_favorite(1469109530)
#test.destroy_favorite(1469109530)

