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
  
    def setToken(self, token, tokenSecret):
        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.setToken(token, tokenSecret)
        self.api = API(self.auth)
    
    def update(self, message):
        message = message.encode("utf-8")
        status = self.api.update_status(message)
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
test.auth()
test.update("oauthupdate-test-测试-----")

