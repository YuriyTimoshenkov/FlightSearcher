import tornado
import json
import Common.authdecorator
from Common.exceptions import  ValidationModelException




class AuthenticationHandler(tornado.web.RequestHandler):


    def post(self):
        loginRequest =  tornado.escape.json_decode(self.request.body)

        #authenticate user
        if loginRequest['login'] == 'Bob':
            token = Common.authdecorator.generate_token(tornado.escape.json_encode({"name": loginRequest['login']}))
            self.write(tornado.escape.json_encode({"token": token}))
        else:
            raise ValidationModelException("Authentication failed.")

    def _handle_request_exception(self, e):
        if isinstance(e, ValidationModelException):
            self.set_status(400, e.message)
            self.finish()
        else:
            raise
