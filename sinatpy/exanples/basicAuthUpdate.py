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
    
    def update(self, message):
        message = message.encode("utf-8")
        status = self.api.update_status(status=message, lat="23.13456", long="113.57679")
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
test.basicAuth('consumer_key', 'username', 'password')
test.update("basicauth-test-测试")

