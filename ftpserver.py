#!/usr/bin/env python
import argparse

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


def start_ftp_server(directory, address, port):
    authorizer = DummyAuthorizer()
    authorizer.add_user(
        "test",
        "test",
        directory,
        perm="elradfmw")
    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer((address, port), handler)
    server.serve_forever()


def main():
    parser = argparse.ArgumentParser(description='Simple FTP server')
    parser.add_argument('directory', help='Publish directory')
    parser.add_argument('-p --port', dest='port', type=int,
                        help='Port number', default=21)
    parser.add_argument('-a --address', dest='address',
                        help='Bind address', default='0.0.0.0')
    args = parser.parse_args()
    start_ftp_server(args.directory, args.address, args.port)


if __name__ == '__main__':
    main()
