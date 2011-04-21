import tornado.web
import os
import urllib
from urlparse import urljoin

import re    
absolute_http_url_re = re.compile(r"^https?://", re.I)

import session
from util import iri_to_uri

class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)
        self.path = ''
        self.session = session.TornadoSession(self.application.session_manager, self)
        
    def get_current_user(self):
        return self.session.get('username')

    def get_user_image(self):
        return self.session.get('me').profile_image_url
    
    def get_user_url(self):
        return self.session.get('me').url
        
    def get_host(self):
        """Returns the HTTP host using the environment or request headers."""
        return self.request.headers.get('Host')
        
    def build_absolute_uri(self, location=None):
        """
        Builds an absolute URI from the location and the variables available in
        this request. If no location is specified, the absolute URI is built on
        ``request.get_full_path()``.
        """
        if not location:
            location = ''
        if not absolute_http_url_re.match(location):
            current_uri = '%s://%s%s' % (self.is_secure() and 'https' or 'http',
                                         self.get_host(), self.path)
            location = urljoin(current_uri, location)
        return iri_to_uri(location)
    
    def is_secure(self):
        return os.environ.get("HTTPS") == "on"
        