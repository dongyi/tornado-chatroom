import tornado.web

import session

class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)
        self.session = session.TornadoSession(self.application.session_manager, self)
        
    def get_current_user(self):
        return self.session.get('username')

    def get_user_image(self):
        return self.session.get('image')