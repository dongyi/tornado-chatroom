import tornado.web

import session
import re
import os
from urlparse import urljoin
import urllib

class Promise(object):
    pass
    
    
absolute_http_url_re = re.compile(r"^https?://", re.I)
#from encoding import smart_str, iri_to_uri, force_unicode
def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Returns a bytestring version of 's', encoded as specified in 'encoding'.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if strings_only and isinstance(s, (types.NoneType, int)):
        return s
    if isinstance(s, Promise):
        return unicode(s).encode(encoding, errors)
    elif not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return ' '.join([smart_str(arg, encoding, strings_only,
                        errors) for arg in s])
            return unicode(s).encode(encoding, errors)
    elif isinstance(s, unicode):
        return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s

def iri_to_uri(iri):
    """
    Convert an Internationalized Resource Identifier (IRI) portion to a URI
    portion that is suitable for inclusion in a URL.

    This is the algorithm from section 3.1 of RFC 3987.  However, since we are
    assuming input is either UTF-8 or unicode already, we can simplify things a
    little from the full method.

    Returns an ASCII string containing the encoded result.
    """
    # The list of safe characters here is constructed from the "reserved" and
    # "unreserved" characters specified in sections 2.2 and 2.3 of RFC 3986:
    #     reserved    = gen-delims / sub-delims
    #     gen-delims  = ":" / "/" / "?" / "#" / "[" / "]" / "@"
    #     sub-delims  = "!" / "$" / "&" / "'" / "(" / ")"
    #                   / "*" / "+" / "," / ";" / "="
    #     unreserved  = ALPHA / DIGIT / "-" / "." / "_" / "~"
    # Of the unreserved characters, urllib.quote already considers all but
    # the ~ safe.
    # The % character is also added to the list of safe characters here, as the
    # end of section 3.1 of RFC 3987 specifically mentions that % must not be
    # converted.
    if iri is None:
        return iri
    return urllib.quote(smart_str(iri), safe="/#%[]=:;$&()+,!?*@'~")

"""
'allow_all_act_msg', 'city', 'created_at', 'description', 'domain', 'favourites_count',
'follow', 'followers', 'followers_count', 'followers_ids', 'following', 'friends', 
'friends_count', 'gender', 'geo_enabled', 'id', 'lists', 'lists_memberships', 'lists_subscriptions', 
'location', 'name', 'parse', 'parse_list', 'profile_image_url', 'province', 'screen_name', 'status', 
'statuses_count', 'timeline', 'unfollow', 'url', 'verified'
"""
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
        # We try three options, in order of decreasing preference.
        if 'HTTP_X_FORWARDED_HOST' in self.request.headers:
            host = self.request.headers.get('HTTP_X_FORWARDED_HOST')
        elif 'HTTP_HOST' in self.request.headers:
            host = self.request.headers.get('HTTP_HOST')
        else:
            # Reconstruct the host using the algorithm from PEP 333.
            host = self.request.headers.get('SERVER_NAME')
            server_port = str(self.request.headers.get('SERVER_PORT'))
            if server_port != (self.is_secure() and '443' or '80'):
                host = '%s:%s' % (host, server_port)
        return host
        
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
        