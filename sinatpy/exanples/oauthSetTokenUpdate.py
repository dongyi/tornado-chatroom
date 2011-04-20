#!/usr/bin/python
#coding=gbk

'''
Created on Aug 2, 2010

@author: ting
'''

import unittest
from weibopy.auth import OAuthHandler
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
     
    def setToken(self, token, tokenSecret):
        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.setToken(token, tokenSecret)
        self.api = API(self.auth)
    
    def update(self, message):
        message = message.encode("utf-8")
        status = self.api.update_status(status=message, lat="30", long="110")
        self.obj = status
        id = self.getAtt("id")
        text = self.getAtt("text")
        print "update---"+ str(id) +":"+ text
        
    def destroy_status(self, id):
        status = self.api.destroy_status(id)
        self.obj = status
        id = self.getAtt("id")
        text = self.getAtt("text")
        print "update---"+ str(id) +":"+ text

test = Test()
#AccessToken的 key和Secret
test.setToken("key", "secret")
test.setToken("322b946d6e9f2761685d6af77fa9b15f", "f41db4efa9e83515de00c261c3a334ca")
test.update("oauth-settokenupdate-test-测试--")

