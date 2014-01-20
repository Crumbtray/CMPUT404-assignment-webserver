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


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        words = self.data.split()
        url = words[1]
        response = self.parseUrl(url)
        self.request.sendall(response)

    # Parses the Url and returns the HTTP Response (either 200 OK, or 404 Not Found)
    def parseUrl(self, url):
        urlWords = url.split("/")
        for word in urlWords:
            if word == "..":
                url = "youtryingtohackme?"

        # If there is no file requested (".") then we are looking for index.html of the directory
        if (urlWords[-1].find(".") == -1):
            if urlWords[-1]:
                url = url + "/"
            url = url + "index.html"
        relative_path = "www" + url

        contentType = relative_path.split(".")[-1]

        content_type_string = "Content-Type: text/"+ contentType +"; charset=UTF-8\r\n"

        try:
            with open(relative_path, 'r') as server_file:
                content = server_file.read()
            content_length = len(content)
            http_header = "HTTP/1.1 200 OK\r\n"
        except IOError:
            http_header = "HTTP/1.1 404 Not Found\r\n"
            with open("404.html", 'r') as not_found_file:
                content = not_found_file.read()
            content_length = len(content)

        # Here we build the HTTP Header:
        
        x_content_words = "X-Content-Type-Options: nosniff\r\n" 
        content_length_string = "Content-Length: " + str(content_length) + "\r\n"
        server_string = "Server: HTTP server\r\n"
        connection_string = "Connection: close\r\n"

        http_response = http_header + content_type_string + x_content_words + content_length_string + server_string + connection_string + "\r\n" + content
        return http_response

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
