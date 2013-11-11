import cherrypy
from cherrypy._cpcompat import ntou
import sys
import database as db
import zlib

def print_help_string():
    print 'Use as follows:\n\n' \
          'python stats_server.py username password host [port]\n'
    
def print_arg_error():
    print 'Arguments incorrect!'
    print_help_string()

# add gzip to allowed content types for decompressing JSON if compressed.
allowed_content_types = [ntou('application/json'),
                         ntou('text/javascript'),
                         ntou('application/gzip')]

class StatHandler(object):
    '''
    A base stat handler for incoming stats. By initialising with a given push function
    the various handlers can be created for different stat types.
    '''
    exposed = True

    def __init__(self, push_fn):
        self.push_fn = push_fn

    def GET(self):
        return 'Hello, World.'

    @cherrypy.tools.json_in(content_type=allowed_content_types, processor=decompress_json)
    def POST(self):
        self.push_fn(cherrypy.serving.request.json, cherrypy.request.remote.ip)
        return 'Hello, World.'


def decompress_json(entity):
    """Try decompressing json before parsing, incase compressed
    content was sent to the server"""

    if not entity.headers.get(ntou("Content-Length"), ntou("")):
        raise cherrypy.HTTPError(411)
    
    body = entity.fp.read()
    # decompress if gzip content type
    if entity.headers.get(ntou("Content-Type")) == ntou("application/gzip"):
        try:
            body = zlib.decompress(body)
        except:
            raise cherrypy.HTTPError(500, 'Invalid gzip data')
    try:
        cherrypy.serving.request.json = json_decode(body.decode('utf-8'))
    except ValueError:
        raise cherrypy.HTTPError(400, 'Invalid JSON document')


def start_cherrypy():
    cherrypy.config.update({'server.socket_port': 8888})
    cherrypy.log('Mounting the handlers')
    method_dispatch_cfg = {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()} }

    function_stat_handler = StatHandler(push_fn_stats)
    handler_stat_handler = StatHandler(push_fn_stats)
    sql_stat_handler = StatHandler(push_sql_stats)

    cherrypy.tree.mount( function_stat_handler(), '/function', method_dispatch_cfg )
    cherrypy.tree.mount( handler_stat_handler(),  '/handler',  method_dispatch_cfg )
    cherrypy.tree.mount( sql_stat_handler(),      '/database', method_dispatch_cfg )
    cherrypy.log('Starting CherryPy')
    try:
        cherrypy.engine.start()
    except IOError:
        logging.error('Unable to bind to address (%s, %d)' % (cfg.cherry_host(), cfg.cherry_port()))
        sys.exit(1)

    cherrypy.engine.wait(cherrypy.process.wspbus.states.STARTED)
    cherrypy.log('CherryPy started')
    cherrypy.engine.block()


if __name__ == '__main__':
    if '--help' in sys.argv:
        print_help_string()
        sys.exit(1)
    if not (len(sys.argv) == 4 or len(sys.argv) == 5):
        print_arg_error()
        sys.exit(1)
        
    username = sys.argv[1]
    password = sys.argv[2]
    host = sys.argv[3]
    port = None
    if len(sys.argv) == 5:
        port = sys.argv[4]
    
    try:
        db.setup_profile_database(username, password, host, port)
        start_cherrypy()
    except Exception, ex:
        print str(ex)