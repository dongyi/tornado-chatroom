import tornado.web

import session

class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)
        self.session = session.TornadoSession(self.application.session_manager, self)
        
    def get_current_user(self):
        user_json = self.session.get('username')
        if not user_json: return None
        return user_json

