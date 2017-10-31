#! /usr/bin/env python

import json
import logging
import random

import concurrent.futures

from http.server import BaseHTTPRequestHandler, HTTPServer


logger = logging.basicConfig(level=logging.DEBUG)

with open('responses.txt') as json_in:
    responses = json.load(json_in)

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        json_string = json.dumps(responses[random.randint(1, 1000)])
        self.wfile.write(bytearray(json_string, 'utf-8'))


def run_server(port):
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, RequestHandler)
    httpd.serve_forever()


def main():
    ports = []
    ports.extend(range(25001, 25301))
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=300)
    pool.map(run_server, ports)


if __name__ == '__main__':
    main()
