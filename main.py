#!/usr/bin/env python
#-*- coding:utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
from tornado.options import define, options
from tornado import ioloop, web
class BaseHandler(tornado.web.RequestHandler):

  def get_login_url(self):
    return u"/login"

  def get_current_user(self):
    user_json = self.get_secure_cookie("user")
    if user_json:
      return tornado.escape.json_decode(user_json)
    else:
      return None

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")
class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home.html")
class LoginHandler(BaseHandler):

  def get(self):
    self.render("login.html", next=self.get_argument("next","/"), message=self.get_argument("error","") )

  def post(self):
    email_usr = self.get_argument("email", "")
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client.Blog
    checkusr = db.users.find({email:email_usr})
    print(db.users.find())
    # if (checkusr==true):
    #     self.redirect(u"/home")
    # else:
    #     print("not found please")

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
  # def set_current_user(self, user):
  #   print ("setting "+user)
  #   if user:
  #     self.set_secure_cookie("user", tornado.escape.json_encode(user))
  #   else:
  #     self.clear_cookie("user")


class RegisterHandler(LoginHandler):

  def get(self):
    self.render(  "register.html", next=self.get_argument("next","/"))

  def post(self):
    email = self.get_argument("email", "")

    already_taken = self.application.syncdb['users'].find_one( { 'user': email } )
    if already_taken:
      error_msg = u"?error=" + tornado.escape.url_escape("Login name already taken")
      self.redirect(u"/login" + error_msg)


    password = self.get_argument("password", "")
    hashed_pass = bcrypt.hashpw(password, bcrypt.gensalt(8))

    user = {}
    user['user'] = email
    user['password'] = hashed_pass

    auth = self.application.syncdb['users'].save(user)
    self.set_current_user(email)

    self.redirect("hello")

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/login", LoginHandler),
        (r"/home", HomeHandler)
    ])
    application.listen(8888)
    ioloop.IOLoop.instance().start()
