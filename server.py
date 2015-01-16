import SocketServer
# coding: utf-8

# Copyright 2015 Jessica Surya, Paul Nhan
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

# CMPUT 410 Winter 2015 Assignment Submission
# Due: January 19. 2015
# Original assignment creators: Abram Hindle, Eddie Antonio Santos
# Assignment Contributors: Jessica Surya (jsurya) , Paul Nhan (pnhan)

import string
import os.path
import time

BASEPATH = "./www"

class MyWebServer(SocketServer.BaseRequestHandler):

    def HTTP200_OK(self, fileLen, fileType):
        self.request.sendall("HTTP/1.1 200 OK\nDate: " + 
            time.strftime("%c") + "\nContent-Type: text/" + fileType + "\n" + "Content-Length: " 
            + str(fileLen) + "\n\n")

    def HTTP404_NOT_FOUND(self):
        self.request.sendall("HTTP/1.1 404 Not Found!\nDate: " + time.strftime("%c") +
            "\nContent-Type: text/html\nContent-Length: 117\n\n" +
            "<html><body>\n<h2>Document not found</h2>\n" +
            "You asked for a document that doesn't exist. " +
            "That is so sad.\n</body></html>\n")

    def HTTP303_Redirect(self, newURL):
        self.request.sendall("HTTP/1.1 303 See Other\nDate: " + time.strftime("%c") +
            "\nLocation: " + newURL +
            "\nContent-Type: text/html\nContent-Length: \n\n" +
            "<html><body>\n<h2>Document Moved</h2>\n" +
            "You asked for a document has moved. " +
            "That is so sad.\n</body></html>\n")

    def request_GET(self):
        args = string.split(self.data, " ")
        filePath = args[1]

        # Normalize paths
        norm_path = os.path.normpath(BASEPATH)
        normalizedPath = os.path.normpath(norm_path + filePath)

        if (os.path.isfile(normalizedPath)) or (os.path.isfile(normalizedPath + "/index.html")):
            # Redirect "/deep" to "/deep/"
            if filePath[-5:] == "/deep":
               newURL = filePath + '/'
               self.HTTP303_Redirect(newURL)

            # Direct paths to directory to index.html file
            if filePath[-1] == '/':
                filePath += "index.html"
                normalizedPath = os.path.normpath(norm_path + filePath)

            fileLen = os.path.getsize(BASEPATH + filePath)
            fileType = filePath.split('.')[-1]

            try:
                reqFile = open(normalizedPath, 'r+')

            except IOError as e:
                print "File could not be opened\n"
                # Display 404 Error as specified in Requirements.org
                self.HTTP404_NOT_FOUND()

            else:
                # Send 200 OK followed by requested file
                self.HTTP200_OK(fileLen, fileType)
                self.request.sendall(reqFile.read())
                reqFile.close()

        else:
            print "404 Not Found!\n"
            self.HTTP404_NOT_FOUND()
        return

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print "Got a request of: %s\n" % self.data

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


