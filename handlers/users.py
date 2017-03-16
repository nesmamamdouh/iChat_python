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
from bson import json_util, ObjectId

class LoginHandler(BaseHandler):
    def get(self):
        self.render("../templates/login.html")
    def post(self):
        email_usr = self.get_argument("email", "")
        password = self.get_argument("password", "")
        checkusr = db.users.find_one({
            '$and': [
                {'email': email_usr},
                {'password': password}
            ]
        })
        if checkusr:
            id_usr = checkusr['_id']
            user = {"id":str(id_usr),"firstname":checkusr['Fname'],"email":email_usr,"lastname":checkusr['Lname'],"friends":checkusr['friends'],"friend_requests":checkusr['friend_requests']}
            self.set_secure_cookie("user", json.dumps(user))
            self.redirect("/home")
        else:
            error_msg = "Login incorrect"
            self.render("../templates/login.html" , error_msg=error_msg)

class RegisterHandler(LoginHandler):
    def get(self):
        self.render(u"../templates/register.html")
    def post(self):
        email = self.get_argument("email", "")
        firstname = self.get_argument("firstname", "")
        lastname = self.get_argument("lastname", "")
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        already_taken = db.users.find({'email':email});
        if already_taken.count() > 0:
          error_msg = {"error_msg":"Email Already Taken"}
          self.set_secure_cookie("error_msg", json_util.dumps(error_msg))
          self.redirect("/register" )
        id_usr = db.users.insert({
            'Fname':firstname,
            'Lname':lastname,
            'email':email,
            'password':str(password),
            'username':username,
            'stat':"on",
            'friends':[],
            'groups':[],
            'friend_requests':[]
        })
        user = {"id":str(id_usr),"firstname":firstname,"email":email,"lastname":lastname,"friends":[],"groups":[],"friend_requests":[]}
        self.set_secure_cookie("user", json.dumps(user))
        self.redirect("/home")

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/login")
class ProfileHandler(BaseHandler):
    def get(self):
        email = self.get_argument("email", "")
        firstname = self.get_argument("firstname", "")
        lastname = self.get_argument("lastname", "")
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        already_taken = db.users.find({'email':email});
        if already_taken.count() > 0:
          error_msg = {"error_msg":"Email Already Taken"}
          self.set_secure_cookie("error_msg", json_util.dumps(error_msg))
          self.render(u"../profile")
    def get(self):
        self.render(u"../templates/profile.html")
