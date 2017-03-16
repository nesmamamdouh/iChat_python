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
class MyFriendsHandler(BaseHandler):
    def get(self):
        usr_info = self.get_secure_cookie("user")
        usr_info = json.loads(usr_info)
        id_usr2 = usr_info['id']
        usr_friend = []
        for user in db.users.find({'_id':ObjectId(id_usr2)}):
            for item in user['friends']:
                myfriends_info =  db.users.find_one({'_id':ObjectId(item)})
                usr_friend.append(myfriends_info)
        self.render(u"../templates/myfriends.html",usr_friend=usr_friend)
class FindFriendsHandler(BaseHandler):
    def get(self):
        usr_info = self.get_secure_cookie("user")
        usr_info = json.loads(usr_info)
        id_usr2 = usr_info['id']
        discoverfriends =  db.users.find({'friends':{'$nin':[id_usr2]}})
        self.render(u"../templates/findfriends.html",discoverfriends=discoverfriends)
class AddFriendsHandler(BaseHandler):
    def get(self):
        usr_info = self.get_secure_cookie("user")
        usr_info = json.loads(usr_info)
        req_id = self.get_argument('user_id')
        id_usr3 = usr_info['id']
        db.users.update({'_id': ObjectId(req_id) }, {"$push" : {'friend_requests': id_usr3 }})
        self.render("../templates/myfriends.html",usr_info=json_util.dumps(usr_info))
class RequestFriendsHandler(BaseHandler):
    def get(self):
        usr_info = self.get_secure_cookie("user")
        usr_info = json.loads(usr_info)
        usr = []
        id_usr4 = usr_info['id']
        for user in db.users.find({'_id':ObjectId(id_usr4)}):
            for item in user['friend_requests']:
                reqfriends_info =  db.users.find_one({'_id':ObjectId(item)})
                usr.append(reqfriends_info)
        self.render(u"../templates/requestfriends.html",usr=usr)
class ConfimFriendsHandler(BaseHandler):
    def get(self):
        usr_info = self.get_secure_cookie("user")
        usr_info = json.loads(usr_info)
        req_con_id = self.get_argument('user_id')
        id_usr5 = usr_info['id']
        confirm_friends = db.users.update({'_id': ObjectId(id_usr5) }, {"$push" : {'friends': req_con_id  }})
        confirm_friends2 = db.users.update({'_id': ObjectId(req_con_id) }, {"$push" : {'friends': id_usr5  }})
        remove_req = db.users.update({'_id': ObjectId(req_con_id) }, {"$pull" : {'friend_requests': id_usr5 }})
        self.redirect("/myfriends")
class RemoveFriendsHandler(BaseHandler):
    def get(self):
        usr_info = self.get_secure_cookie("user")
        usr_info = json.loads(usr_info)
        rem_con_id = self.get_argument('user_id')
        id_usr6 = usr_info['id']
        remove_friend = db.users.update({'_id': ObjectId(id_usr6) }, {"$pull" : {'friends': rem_con_id }})
        self.redirect("/myfriends")
