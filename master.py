#!/usr/bin/python
# -*- coding: utf-8 -*-

import SocketServer

from TCPHandler import UploadTCPHandler

if __name__ == "__main__":
    HOST, PORT = "localhost", 9998

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), UploadTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()



