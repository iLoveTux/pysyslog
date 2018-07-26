# -*- coding: utf-8 -*-

"""Main module."""
import ssl
import sys
import json
import logging
import logging.config
import socketserver

# Optimizations
logging.logThreads = 0
logging.logProcesses = 0
logging._srcfile = None
logging.logMultiprocessing = 0
logging.raiseExceptions = False

__all__ = [
    "log_writer",
    "ThreadedTCPServer",
    "ThreadedTCPRequestHandler",
]

def log_writer(q, logging_config):
    # Optimizations
    logging.logThreads = 0
    logging.logProcesses = 0
    logging._srcfile = None
    logging.logMultiprocessing = 0
    logging.raiseExceptions = False
    if logging_config:
        with open(logging_config, "r") as fin:
            logging.config.dictConfig(json.load(fin))
    else:
        logging.basicConfig(stream=sys.stdout, level=20)
    while True:
        loggername, msg = q.get()
        logging.getLogger(loggername).info(msg.strip().decode())
        q.task_done()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, queue, *args, **kwargs):
        self.queue = queue
        socketserver.TCPServer.__init__(self, *args, **kwargs)

    def get_request(self):
        if hasattr(self, "certfile") and hasattr(self, "keyfile"):
            (socket, addr) = socketserver.TCPServer.get_request(self)
            return (
                ssl.wrap_socket(
                    socket,
                    server_side=True,
                    certfile=self.certfile,
                    keyfile=self.keyfile,
                ),
                addr
            )
        else:
            return socketserver.TCPServer.get_request(self)

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(self.queue, request, client_address, self)

    def server_close(self):
        self.socket.close()
        self.shutdown()
        return SocketServer.TCPServer.server_close(self)

class QueuedTCPRequestHandler(socketserver.StreamRequestHandler):

    def __init__(self, queue, *args, **kwargs):
        self.queue = queue
        socketserver.StreamRequestHandler.__init__(self, *args, **kwargs)

    def handle(self):
        _loggername = self.client_address[0].encode().decode()
        for line in self.rfile:
            self.queue.put((_loggername, line))

    def finish(self):
        self.request.close()
