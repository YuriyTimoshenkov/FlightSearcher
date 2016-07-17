import tornado
import sys, traceback
from Common.exceptions import  ValidationModelException


class BaseHandler(tornado.web.RequestHandler):
    def _handle_request_exception(self, e):
        self.logger.error(e)

        if isinstance(e, ValidationModelException):
            self.set_status(400, e.message)
            self.write(e.message)
            self.finish()
        else:
            self.set_status(500)

            formatted_lines = traceback.format_exc().splitlines()
            self.write(formatted_lines[-1])
            self.finish()

    def get_current_user(self):
        return self.currentUser
