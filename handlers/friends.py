import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import os
import json
from tornado.options import define, options
from tornado import ioloop, web
from handlers.base import *
from handlers.database import *

class MyFriendsHandler(BaseHandler):
    def get(self):
        user = self.get_secure_cookie("user")
        user = json.loads(user)
        print(user['id'])
        self.render(u"../templates/myfriends.html")
class FindFriendsHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.render(u"../templates/findfriends.html")
