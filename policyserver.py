#!/usr/bin/env python
import sys
import socket
from optparse import OptionParser

POLICY_DATA = """<?xml version="1.0"?>
<cross-domain-policy>
    <site-control permitted-cross-domain-policies="all"/>
    <allow-access-from domain="*" to-ports="*" />
</cross-domain-policy>"""

DEFAULT_ADDR = '0.0.0.0'
DEFAULT_PORT = 1234

RECV_SIZE = 1024


class PolicyServer(object):
    def __init__(self, bind_address, bind_port, backlog=None):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind_address = bind_address
        self.bind_port = bind_port
        self.backlog = backlog or 1

    def start(self):
        self.socket.bind((self.bind_address, self.bind_port))
        self.socket.listen(self.backlog)
        try:
            while True:
                connection, address = self.socket.accept()
                try:
                    self.handle(connection, address)
                finally:
                    connection.close()
        except KeyboardInterrupt:
            sys.exit()

    def handle(self, connection, address):
        sys.stdout.write('CONNECT from %s\n' % address[0])
        data = connection.recv(RECV_SIZE)
        sys.stdout.write('recv data %d bytes from %s\n' % (
            len(data), address[0]))
        connection.send(POLICY_DATA)


class PolicyServerCommand(object):
    SERVER_CLASS = PolicyServer

    def __init__(self):
        self.parser = OptionParser()

        self.parser.add_option(
            '--address',
            dest='address',
            default=DEFAULT_ADDR,
            help='bind address')

        self.parser.add_option(
            '--port',
            dest='port',
            default=DEFAULT_PORT,
            type='int',
            help='port number')

    def main(self):
        options, args = self.parser.parse_args()
        bind_address = options.address
        bind_port = options.port
        self.server = self.SERVER_CLASS(bind_address, bind_port)
        sys.stdout.write('Starting policyserver addr=%s, port=%s ...\n' % (
            bind_address, bind_port))
        self.server.start()


if __name__ == '__main__':
    PolicyServerCommand().main()
