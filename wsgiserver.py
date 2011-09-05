# coding: utf-8
import os

from optparse import OptionParser
from wsgiref import simple_server

##########################
# django.utils.importlib
##########################

# Taken from Python 2.7 with permission from/by the original author.
import sys

def _resolve_name(name, package, level):
    """Return the absolute name of the module to be imported."""
    if not hasattr(package, 'rindex'):
        raise ValueError("'package' not set to a string")
    dot = len(package)
    for x in xrange(level, 1, -1):
        try:
            dot = package.rindex('.', 0, dot)
        except ValueError:
            raise ValueError("attempted relative import beyond top-level "
                              "package")
    return "%s.%s" % (package[:dot], name)


def import_module(name, package=None):
    """Import a module.

    The 'package' argument is required when performing a relative import. It
    specifies the package to use as the anchor point from which to resolve the
    relative import to an absolute import.

    """
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1
        name = _resolve_name(name[level:], package, level)
    __import__(name)
    return sys.modules[name]

##########################

def split_names(path):
    return path.split(':')


def get_application(path):
    module_path, app_name = split_names(path)
    module = import_module(module_path)
    return getattr(module, app_name)


def run(host, port, app):
    server = simple_server.make_server(host, port, app)
    server.serve_forever()


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--host', dest='host', default='localhost', help='hostname')
    parser.add_option('--port', dest='port', default=8000,
        type='int', help='port number')

    options, args = parser.parse_args()

    if len(args) < 1:
        print "%s [options] <module>:<application>" % os.path.basename(__file__)
        sys.exit()

    app = get_application(args[0])

    print "Serving HTTP on", options.host, "port", options.port, "..."

    run(options.host, options.port, app)
