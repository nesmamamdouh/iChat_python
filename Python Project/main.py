import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import os
from tornado.options import define, options
from tornado import ioloop, web

class BaseHandler(tornado.web.RequestHandler):
  def get_login_url(self):
    return u"templates/login"

  def get_current_user(self):
    user_json = self.get_secure_cookie("user")
    if user_json:
      return tornado.escape.json_decode(user_json)
    else:
      return None

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/login.html")
class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/home.html")
class LoginHandler(BaseHandler):

  def get(self):
    self.render("templates/login.html", next=self.get_argument("next","/"), message=self.get_argument("error","") )

  def post(self):
    email_usr = self.get_argument("email", "")
    password = self.get_argument("password", "")
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client.Blog
    checkusr = db.users.find({'email':email_usr});
    # for record in checkusr:
    #     print(record['name'])
    if checkusr.count() > 0:
        self.redirect(u"/home")
    else:
        error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect.")
        self.redirect(u"/login" + error_msg)


    # return email
  #   user = self.application.syncdb['users'].find_one( { 'user': email } )
  #
  #   if user and user['password'] and bcrypt.hashpw(password, user['password']) == user['password']:
  #     self.set_current_user(email)
  #     self.redirect("hello")
  #   else:
  #     error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect.")
  #     self.redirect(u"/login" + error_msg)
  #
  def set_current_user(self, user):
    print ("setting "+user)
    if user:
      self.set_secure_cookie("user", tornado.escape.json_encode(user))
    else:
      self.clear_cookie("user")


class RegisterHandler(LoginHandler):
  def get(self):
    self.render(u"templates/register.html")

  def post(self):
    email = self.get_argument("email", "")
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client.Blog
    already_taken = db.users.find({'email':email});
    if already_taken.count() > 0:
      error_msg = u"?error=" + tornado.escape.url_escape("Login name already taken")
      self.redirect(u"templates/register" + error_msg)
    password = self.get_argument("password", "")
    # hashed_pass = bcrypt.hashpw(password, bcrypt.gensalt(8))
    db.users.insert({
        'email':email,
        'password':password
    })
    # self.set_current_user(email)
    self.redirect(u"templates/home")
class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.render(u"templates/login.html")

class MyGroupsHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.render("templates/mygroups.html")

class DiscoverGroupsHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.render("templates/discovergroups.html")
class MyFriendsHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.render(u"templates/myfriends.html")
class FindFriendsHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.render(u"templates/findfriends.html")
# if __name__ == "__main__":
app = web.Application([
		(r"/", MainHandler),
        (r"/login", LoginHandler),
        (r"/home", HomeHandler),
        (r"/register", RegisterHandler),
        (r"/logout", LogoutHandler),
        (r"/mygroups", MyGroupsHandler),
        (r"/discovergroups", DiscoverGroupsHandler),
        (r"/myfriends", MyFriendsHandler),
        (r"/findfriends", FindFriendsHandler)
	],static_path='static',debug=True,cookie_secret= 'Settings.COOKIE_SECRET')
app.listen(8888)
ioloop.IOLoop.current().start()





        # handlers = [
        #     (r"/", MainHandler),
        #     (r"/templates/login", LoginHandler),
        #     (r"/templates/home", HomeHandler),
        #     (r"/templates/register", RegisterHandler),
        #     (r"/templates/logout", LogoutHandler)
        # ]
        #
        # settings = {
        #      "static_path": os.path.join(os.path.dirname(__file__), "static"),
        #      "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__"
        #     }
        # tornado.web.Application.__init__(self, handlers, **settings)
