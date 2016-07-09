import tornado
from Common.exceptions import  ValidationModelException


class BaseHandler(tornado.web.RequestHandler):
    def _handle_request_exception(self, e):
        if isinstance(e, ValidationModelException):
            self.set_status(400, e.message)
            self.finish()
        else:
            raise

    def get_current_user(self):
        return self.currentUser
