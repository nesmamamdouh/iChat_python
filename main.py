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
from handlers.ajax import APIHandler
from handlers.sse import EventHandler,SSEHandler
from handlers.chat import ChatHandler,WSHandler

class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)

class HomeHandler(MainHandler):
    def get(self):
        self.render(u"templates/home.html")

app = web.Application([
		(r"/", MainHandler),
        (r"/login", LoginHandler),
        (r"/home", HomeHandler),
        (r"/register", RegisterHandler),
        (r"/logout", LogoutHandler),
        (r"/chat", ChatHandler),
        (r"/mygroups", MyGroupsHandler),
        (r"/myapi", APIHandler),
        (r"/sse", SSEHandler),
        (r"/event", EventHandler),
        (r"/chat", ChatHandler),
        (r"/ws", WSHandler),
        (r"/discovergroups", DiscoverGroupsHandler),
        (r"/myfriends", MyFriendsHandler),
        (r"/findfriends", FindFriendsHandler),
        (r"/profile", ProfileHandler),
        (r"/addfriend", AddFriendsHandler),
        (r"/requestfriends", RequestFriendsHandler),
        (r"/addfriend_request", ConfimFriendsHandler),
        (r"/removefriend", RemoveFriendsHandler),
        (r"/addtogroup", AddToGroupHandler)
	],static_path='static',debug=True,cookie_secret= 'Settings.COOKIE_SECRET')
app.listen(8888)
ioloop.IOLoop.current().start()
