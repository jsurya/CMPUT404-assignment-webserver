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
import time

class MyWebServer(SocketServer.BaseRequestHandler):

    def HTTP200_OK(self, fileLen):
        self.request.sendall("HTTP/1.1 200 OK\nDate: " + 
            time.strftime("%c") + "\n Content-Type: text/html\n" + "Content-Length: " + str(fileLen))

    def HTTP404_NOT_FOUND(self):
        self.request.sendall("HTTP/1.1 404 Not Found!\nDate: " + time.strftime("%c") +
            "\nContent-Type: text/html\nContent-Length: 117\n\n" +
            "<html><body>\n<h2>Document not found</h2>\n" +
            "You asked for a document that doesn't exist. " +
            "That is so sad.\n</body></html>\n")

    def request_GET(self):
        args = string.split(self.data, " ")
        filePath = args[1]
        print filePath

        if os.path.exists('.' + filePath):
            print "200 OK\n"
            fileLen = os.path.getsize('.' + filePath)
            print fileLen
            self.HTTP200_OK(fileLen)
            reqFile = open('.' + filePath, 'w')
            self.request.sendall(reqFile)
            reqFile.close()

        else:
            print "404 Not Found!\n"
            self.HTTP404_NOT_FOUND()
            
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


