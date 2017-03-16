from tornado import gen,web,iostream

import random,json,time

class EventHandler(web.RequestHandler):
    def get(self):
        self.render('../templates/sse.html')

class SSEHandler(web.RequestHandler):
    def initialize(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Content-Type', 'text/event-stream')
        self.set_header('Cache-Control', 'no-cache')
    @gen.coroutine
    def get(self):
        while True:
            try:  
                data= 'id:13\n'
                data+= 'event:newPost\n'
                data+= 'retry: 15000\n'
                fl = open("file.txt",'r')
                data += 'data: {0}\n\n'.format(fl.read())
                print("Hi There")
                yield gen.sleep(3)
                self.write(data)
                yield self.flush()
            except iostream.StreamClosedError:
                print("Bye There")
                break