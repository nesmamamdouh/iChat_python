from tornado import web,websocket
from bson import json_util, ObjectId
import json
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import os
from tornado.options import define, options
from tornado import ioloop, web
from handlers.base import *
from handlers.database import *
clients = {}
class WSHandler(websocket.WebSocketHandler):
	def open(self):
		user = self.get_secure_cookie("user")
		usr_info=json.loads(user)
		if (self.get_argument("g") in clients):
			clients[self.get_argument("g")].append(self);
		else:
			clients[self.get_argument("g")]=[];
			clients[self.get_argument("g")].append(self);
		fl= open("../file"+self.get_argument("g")+".txt",'w');
		i=0;
		fl.write("all"+"\n");
		for c in clients[self.get_argument("g")]:
			fl.write(usr_info['firstname']+'\n');
			i+=1;
		fl.close();
	def on_message(self,message):
		if message.split(":")[1]=="-1":
			for c in clients[self.get_argument("g")]:
				c.write_message(message)
		else:
			clients[self.get_argument("g")][int(message.split(":")[1])].write_message(message);
			self.write_message(message);

	def on_close(self):
		print(clients[self.get_argument("g")]);
		if (self in clients[self.get_argument("g")]):
			clients[self.get_argument("g")].remove(self);
			for c in clients[self.get_argument("g")]:
				c.write_message("sorry guys!! someone closed !!")

class ChatHandler(BaseHandler):
	def get(self):
		usr_info = self.get_secure_cookie("user")
		usr_info = json.loads(usr_info)
		self.render(u"../templates/chat.html",usr_info=json_util.dumps(usr_info),g=self.get_argument("g"))
