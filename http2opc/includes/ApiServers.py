from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import json
import urllib
from includes.mTools import Thread
import thread
from ApiFunctions import ApiFunctions

me = {"name": "bing"}
#mainpanel = None
#port = 8003
#host = ''
logger = None
funcs = None

class RestApiServer(Thread):
    def __init__(self, console, server_ip = '', server_port = 8003):

        #self.logger = logger
        global logger
        logger = console

        self.server_ip = server_ip
        self.server_port = server_port

        httpd = HTTPServer((self.server_ip, self.server_port), RestRequestHandler)
        logger.info('Started REST API Server on port ' + str(self.server_port))

        global funcs
        funcs = ApiFunctions(logger)
        result = funcs.init()

        if result:
            httpd.serve_forever()




class RestRequestHandler (BaseHTTPRequestHandler) :

    def do_GET(self) :

        params = []

        #logger.info('Hit with: ' + self.path )
        qstring = self.path[1:].split('&')
        for s in qstring:

            if '=' in s:

                k,v = s.split('=')
                if k == 'method':
                    method = v
                else:
                    params = v
            else:
                method = False
                params = False

        #send response code:
        self.send_response(200)
        #send headers:
        #self.send_header("Content-type:", "text/html")
        self.send_header("Content-type:", "application/json")
        # send a blank line to end headers:
        self.wfile.write("\n")

        ## -- Extract function parameters. 
        if method:

            if params:
                d_params = urllib.unquote(params).decode('utf8').replace('+', ' ')

            if method.lower() == 'list':
                json.dump( funcs.list(d_params), self.wfile )
            elif method.lower() == 'listrecursive':
                json.dump( funcs.listRecursive(d_params), self.wfile ) 
            elif method.lower() == 'listtree':
                json.dump( funcs.listTree(d_params), self.wfile )
            elif method.lower() == 'listonedeep':
                json.dump( funcs.listOneDeep(d_params), self.wfile )
            elif method.lower() == 'read':
                json.dump( funcs.read(d_params), self.wfile ) 
            elif method.lower() == 'properties':
                json.dump( funcs.properties(d_params, False), self.wfile )
            elif method.lower() == 'jsonproperties':
                json.dump( funcs.properties(d_params, True), self.wfile )
            elif method.lower() == 'search':
                json.dump( funcs.search(d_params), self.wfile )
            elif method.lower() == 'testing':
                json.dump( funcs.testing(d_params), self.wfile )
            elif method.lower() == 'testcall':
                json.dump( funcs.test_call(), self.wfile )




    def log_message(self, format, *args):
        logger.info('Incoming: ' + self.client_address[0] )
        #logger.info('Incoming: ' + self.client_address[0] + ' - ' + format%args )

