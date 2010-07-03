import os
import sys
import asyncore
from datetime import datetime
from optparse import OptionParser
from smtpd import SMTPServer, DebuggingServer

class EmailServer(SMTPServer):
    no = 0

    def __init__(self, localaddr, remoteaddr, output_dir=None):
        SMTPServer.__init__(self, localaddr, remoteaddr)
        if not output_dir:
            output_dir = '.'
        self.output_dir = output_dir

    def process_message(self, peer, mailfrom, rcpttos, data):
        filename = '%s-%d.eml' % (datetime.now().strftime('%Y%m%d%H%M%S'), self.no)
        fullpath = os.path.normpath(os.path.join(self.output_dir, filename))
        f = open(fullpath, 'w')
        f.write(data)
        f.close()
        sys.stdout.write('%s saved.\n' % filename)
        self.no += 1

def run(host, port, debug=True, outdir=None):
    kwargs = {
        'localaddr': (host, port),
        'remoteaddr': None,
    }

    if debug:
        server_class = DebuggingServer
    else:
        server_class = EmailServer
        kwargs['output_dir'] = outdir

    server = server_class(**kwargs)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option('--host', dest='host', default='localhost', help='hostname')
    parser.add_option('--port', dest='port', default=8025, help='port number')
    parser.add_option('--outdir', dest='outdir', default='.', help='output directory')
    parser.add_option('--debug', action='store_true', dest='debug', help='use DebuggingServer')

    options, args = parser.parse_args()

    run(options.host, options.port, options.debug, options.outdir)
