#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from sina_auth import OAuthHandler
#import sina_oauth as oauth 
#WeibopError
from weibopy import OAuthHandler, oauth, WeibopError
from tornado.options import define, options
from base import BaseHandler
import tornado.web
from weibopy.api import API


class WebOAuthHandler(OAuthHandler):
    def get_authorization_url_with_callback(self, callback, signin_with_twitter=False):
        """Get the authorization URL to redirect the user"""
        try:
            # get the request token
            self.request_token = self._get_request_token()
            # build auth request and return as url
            if signin_with_twitter:
                url = self._get_oauth_url('authenticate')
            else:
                url = self._get_oauth_url('authorize')
            request = oauth.OAuthRequest.from_token_and_callback(
                token=self.request_token, callback=callback, http_url=url
            )
            return request.to_url()
        except Exception, e:
            raise WeibopError(e)


def _get_referer_url(request_handle):
    headers = request_handle.request.headers
    referer_url = headers.get('HTTP_REFERER', '/')
    host = headers.get('Host')
    if referer_url.startswith('http') and host not in referer_url:
        referer_url = '/' # 避免外站直接跳到登录页而发生跳转错误
    return referer_url

def _oauth():
    """获取oauth认证类"""
    return WebOAuthHandler(options.SINA_APP_KEY, options.SINA_APP_SECRET)


class AuthLoginCheckHandler(BaseHandler):
    def get(self):
        verifier = str(self.get_argument('oauth_verifier', None))
        auth_client = _oauth()
        # 设置之前保存在session的request_token
        print self.session
        request_token = self.session['oauth_request_token']
        del self.session['oauth_request_token']
        self.session.save()
        auth_client.set_request_token(request_token.key, request_token.secret)

        access_token = auth_client.get_access_token(verifier)
        current_user = auth_client.get_username()
        api = API(auth_client)

        self.session['me'] = api.me()
        self.session['username'] = current_user

        # 保存access_token，以后访问只需使用access_token即可
        self.session['oauth_access_token'] = access_token
        self.session.save()
        # 跳转回最初登录前的页面
        back_to_url = self.session.get('login_back_to_url', '/')
        return self.redirect(back_to_url)



class AuthLoginHandler(BaseHandler):
    def get(self):
        back_to_url = _get_referer_url(self)
        self.session['login_back_to_url'] = back_to_url

        # TODO: 要实现一个类似django里build_absulote_url的方法
        login_backurl = 'http://192.168.33.24:8000/wblogin_check'
        auth_client = _oauth()

        auth_url = auth_client.get_authorization_url_with_callback(login_backurl)
        self.session['oauth_request_token'] = auth_client.request_token
        self.session.save()
        return self.redirect(auth_url)
        


class AuthLogoutHandler(BaseHandler):
    def get(self):
        del self.session['oauth_access_token']
        self.session.save()
        back_to_url = _get_referer_url(self)
        self.write("You are now logged out")



def login_required(func):
    def new_func(*argc, **argkw):
        # check if the user logined
        request = argc[0]
        access_token = request.session.get('oauth_access_token')
        if access_token is None:
            return request.render("login.html")
        return func(*argc, **argkw)
    return new_func

