from tornado import gen,web
import json,os,time

class APIHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        print("===================================file")
        clm = float(self.get_query_argument('lastmod'));
        id_g = self.get_query_argument('id');
        slm, data = os.path.getmtime("../file'"+id_g+"'.txt"),{}
        while( slm <= clm):
            print("file before sleep")
            yield gen.sleep(0.5)
            print("file after sleep")
            slm = os.path.getmtime("../file'"+id_g+"'.txt")
            print("file mtime= "+str(slm))
        print("======================file out of loop")
        fl = open("../file'"+id_g+"'.txt",'r')
        data['body'] = fl.read()
        data['lastmod'] = slm;
        fl.close()
        self.write(data)


    def post(self):
        pass
