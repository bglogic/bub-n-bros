from __future__ import nested_scopes
import os, urllib, socket
import BaseHTTPServer
from SimpleHTTPServer import *


pathloaders = {}

def fileloader(filename, mimetype='application/octet-stream'):
    if mimetype.startswith('text/'):
        mode = 'r'
    else:
        mode = 'rb'
    def load():
        return open(filename, mode), mimetype
    return load

def register(url, loader):
    if url.startswith('/'):
        url = url[1:]
    pathloaders[url] = loader


class MiniHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        url = urllib.unquote(self.path)
        if url.startswith('/'):
            url = url[1:]
        if url not in pathloaders:
            self.send_error(404, "File not found")
            return None
        try:
            f, ctype = pathloaders[url]()
        except IOError:
            self.send_error(404, "I/O error")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        self.end_headers()
        return f


def runserver(port=8000, HandlerClass=MiniHandler,
              ServerClass=BaseHTTPServer.HTTPServer):
    server_address = ('', port)
    try:
        httpd = ServerClass(server_address, HandlerClass)
    except socket.error:
        return None
    return httpd.fileno(), httpd.handle_request
