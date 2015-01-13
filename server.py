import SocketServer
# coding: utf-8

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

import string
import os.path
import urllib
import urllib2
import httplib

class MyWebServer(SocketServer.BaseRequestHandler):

    def request_GET(self):
        args = string.split(self.data, " ")
        file_path = args[1]
        print file_path

        if os.path.exists('.' + file_path) == True:
            if os.path.isfile('.' + file_path) == True:
                print "Valid file\n"
                self.request.sendall("Valid file\n")
        
            else:
                print "200 OK Not FOUND!\n"
                self.request.sendall("200 OK Not FOUND!\n")
        else:
            print "404 Not Found!\n"
            self.request.sendall("404 Not Found!\n")
            self.request.sendall(httplib.responses[httplib.NOT_FOUND])

        return

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print "Got a request of: %s\n" % self.data

        # client_request = urllib2.urlopen(self.data)
        # print client_request.info()
        # html = client_request.read()

        if string.find(self.data, "GET /") == 0:
            self.request_GET()

        return



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()


