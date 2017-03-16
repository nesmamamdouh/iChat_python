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
from bson import json_util, ObjectId
from handlers.base import *

class MyGroupsHandler(BaseHandler):
    def get(self):
        usr_info = self.get_secure_cookie("user")
        usr_info = json.loads(usr_info)
        checkgroups = db.groups.find({'member':{'$all':[usr_info['id']]}});
        self.render("../templates/mygroups.html",checkgroups=checkgroups,usr_info=json_util.dumps(usr_info))

class DiscoverGroupsHandler(BaseHandler):
    def get(self):
        usr_info = self.get_secure_cookie("user")
        usr_info = json.loads(usr_info)
        discovergroups =  db.groups.find({'member':{'$nin':[usr_info['id']]}})
        self.render("../templates/group.html",discovergroups=discovergroups,usr_info=json_util.dumps(usr_info))
class AddToGroupHandler(BaseHandler):
    def get(self):
        usr_info = self.get_secure_cookie("user")
        usr_info = json.loads(usr_info)
        req_group_id = self.get_argument('group_id')
        id_usr5 = usr_info['id']
        print(req_group_id)
        print(id_usr5)
        confirm_group = db.groups.update({'_id': ObjectId(req_group_id) }, {"$push" : {'member': str(id_usr5)  }})
        self.redirect("/discovergroups")
