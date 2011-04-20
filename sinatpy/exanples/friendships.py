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
        self.authType = 'basicauth'
        self.auth = BasicAuthHandler(username, password)
        self.api = API(self.auth,source=source)
          
    def setToken(self, token, tokenSecret):
        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.setToken(token, tokenSecret)
        self.api = API(self.auth)
    
    
    def create_friendship(self):
        user = self.api.create_friendship(id=1773365880)
        self.obj = user
        uid = self.getAtt("id")
        screen_name = self.getAtt("screen_name")
        print "create_friendship---"+ str(uid) +":"+ screen_name
        
    def destroy_friendship(self):
        user = self.api.destroy_friendship(id=1773365880)
        self.obj = user
        uid = self.getAtt("id")
        screen_name = self.getAtt("screen_name")
        print "destroy_friendship---"+ str(uid) +":"+ screen_name
        
    def exists_friendship(self):
        self.obj = self.api.exists_friendship(user_a=1772333754, user_b=1773365880)
        friends = self.getAtt("friends")
        print "exists_friendship--- "+ str(friends)
        
    def show_friendship(self):
        showList = self.api.show_friendship(target_id=1773365880)
        for obj in showList:
            self.obj = obj
            uid = self.getAtt("id")
            screen_name = self.getAtt("screen_name")
            print "show_friendship---"+ str(uid) +":"+ screen_name


test = Test()
#AccessToken的 key和Secret
test.setToken("key", "secret")
#test.create_friendship()
test.show_friendship()
test.exists_friendship()
#test.destroy_friendship()


