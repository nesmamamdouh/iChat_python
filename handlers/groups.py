import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import os
import json
from tornado.options import define, options
from tornado import ioloop, web
from handlers.database import *

class BaseHandler(tornado.web.RequestHandler):
  def get_login_url(self):
      return u"../templates/login"
  def get_current_user(self):
      return self.get_secure_cookie("user")

class MyGroupsHandler(BaseHandler):
    def get(self):
        usr_info = self.get_secure_cookie("user")
        usr_info = json.loads(usr_info)
        print(usr_info['id'])
        checkgroups = db.groups.find({"members":{'$elemMatch':{"$in":[usr_info['id']]}}});
        self.render("../templates/mygroups.html")

class DiscoverGroupsHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.render("../templates/discovergroups.html")
