#!//usr/bin/env python
#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import tornado.web
from base import BaseHandler
import tornado.escape
from weibopy.api import API
Member = {}
class MemberHandler():
    global Member
    def memberadd(self,userid,user={}):
        Member[userid]=user

    def memberrm(self,userid):
        del(Member[userid])

    def membershow(self):
        return Member

mem = MemberHandler()

   
def main():
    print mem.Member

    
if "__main__" == __name__:
    main()




