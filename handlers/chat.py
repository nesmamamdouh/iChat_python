from tornado import web,websocket
from bson import json_util, ObjectId
import json

clients = {}
class WSHandler(websocket.WebSocketHandler):
	def open(self):
		user = self.get_secure_cookie("user")
		usr_info=json.loads(user)
		#clients.add(self.get_argument("g"):[]);
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

class ChatHandler(web.RequestHandler):
	def get(self):
		user = self.get_secure_cookie("user")
		self.render(u"../templates/chat.html",user=user,g=self.get_argument("g"))
