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
    def setToken(self, token, tokenSecret):
        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.setToken(token, tokenSecret)
        self.api = API(self.auth)
        
    def basicAuth(self, source, username, password):
        self.auth = BasicAuthHandler(username, password)
        self.api = API(self.auth,source=source)
        
    def auth(self):
        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth_url = self.auth.get_authorization_url()
        print 'Please authorize: ' + auth_url
        verifier = raw_input('PIN: ').strip()
        self.auth.get_access_token(verifier)
        self.api = API(self.auth)
        
    def friends_timeline(self):
        timeline = self.api.friends_timeline(count=2, page=1)
        for line in timeline:
            self.obj = line
            mid = self.getAtt("id")
            text = self.getAtt("text")
            print "friends_timeline---"+ str(mid) +":"+ text

    def comments_timeline(self):
        timeline = self.api.comments_timeline(count=2, page=1)
        for line in timeline:
            self.obj = line
            mid = self.getAtt("id")
            text = self.getAtt("text")
            print "comments_timeline---"+ str(mid) +":"+ text
            
    def user_timeline(self):
        timeline = self.api.user_timeline(count=20, page=1)
        for line in timeline:
            self.obj = line
            mid = self.getAtt("id")
            text = self.getAtt("text")
            created_at = self.getAtt("created_at")
            print "user_timeline---"+ str(mid) +":"+ str(created_at)+":"+ text
        timeline = self.api.user_timeline(count=20, page=2)
        for line in timeline:
            self.obj = line
            mid = self.getAtt("id")
            text = self.getAtt("text")
            created_at = self.getAtt("created_at")
            print "user_timeline---"+ str(mid) +":"+ str(created_at)+":"+ text
            
        timeline = self.api.user_timeline(count=20, page=3)
        for line in timeline:
            self.obj = line
            mid = self.getAtt("id")
            text = self.getAtt("text")
            created_at = self.getAtt("created_at")
            print "user_timeline---"+ str(mid) +":"+ str(created_at)+":"+ text
            
    def public_timeline(self):
        timeline = self.api.public_timeline(count=2, page=1)
        for line in timeline:
            self.obj = line
            mid = self.getAtt("id")
            text = self.getAtt("text")
            print "public_timeline---"+ str(mid) +":"+ text


test = Test()
#AccessToken的 key和Secret
test.setToken("key", "secret")
test.comments_timeline()
test.friends_timeline()
test.user_timeline()
test.public_timeline()

