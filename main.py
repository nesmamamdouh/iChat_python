import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import os
import json
from tornado.options import define, options
from tornado import ioloop, web
from handlers.groups import *
from handlers.base import *
from handlers.friends import *
from handlers.database import *
from handlers.users import *

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        user = self.get_secure_cookie("user")
        self.render(u"templates/home.html",user=user)

app = web.Application([
		(r"/", MainHandler),
        (r"/login", LoginHandler),
        (r"/home", HomeHandler),
        (r"/register", RegisterHandler),
        (r"/logout", LogoutHandler),
        (r"/mygroups", MyGroupsHandler),
        (r"/discovergroups", DiscoverGroupsHandler),
        (r"/myfriends", MyFriendsHandler),
        (r"/findfriends", FindFriendsHandler),
        (r"/profile", ProfileHandler)
	],static_path='static',debug=True,cookie_secret= 'Settings.COOKIE_SECRET')
app.listen(8888)
ioloop.IOLoop.current().start()
