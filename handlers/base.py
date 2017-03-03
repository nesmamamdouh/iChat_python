import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import os
import json
from tornado.options import define, options
from tornado import ioloop, web

class BaseHandler(tornado.web.RequestHandler):
    def get_login_url(self):
      return u"../templates/login"
    def get_current_user(self):
      return self.get_secure_cookie("user")
