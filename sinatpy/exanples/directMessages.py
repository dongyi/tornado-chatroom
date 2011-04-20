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
        
    def direct_message(self):
        messages = self.api.direct_messages()
        for msg in messages:
            self.obj = msg
            mid = self.getAtt("id")
            text = self.getAtt("text")
            print "direct_message---"+ str(mid) +":"+ text
            
    def sent_direct_messages(self):
        messages = self.api.sent_direct_messages()
        for msg in messages:
            self.obj = msg
            mid = self.getAtt("id")
            text = self.getAtt("text")
            print "sent_direct_messages---"+ str(mid) +":"+ text
            
    def new_direct_message(self):
        msg = self.api.new_direct_message(id=1772333754,text='abc921')
        self.obj = msg
        mid = self.getAtt("id")
        text = self.getAtt("text")
        print "new_direct_message---"+ str(mid) +":"+ text
            
    def destroy_direct_message(self, id):
        msg = self.api.destroy_direct_message(id)
        self.obj = msg
        mid = self.getAtt("id")
        text = self.getAtt("text")
        print "destroy_direct_message---"+ str(mid) +":"+ text


test = Test()
#AccessToken的 key和Secret
test.setToken("key", "secret")
test.direct_message()
#test.sent_direct_messages()
#test.new_direct_message()
#test.destroy_direct_message(180198972)