import tornado.web

import session


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
        self.session = session.TornadoSession(self.application.session_manager, self)
        
    def get_current_user(self):
        return self.session.get('username')

    def get_user_image(self):
        return self.session.get('me').profile_image_url
    
    def get_user_url(self):
        return self.session.get('me').url