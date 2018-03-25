from BaseHTTPServer import BaseHTTPRequestHandler
import BaseHTTPServer
import urlparse
import geocode as gc
import threading
import urllib2
import json
import time



class GeoServiceHTTPReqHandler(BaseHTTPRequestHandler):
    """ Used to handle get requests to return geocodes
    """

    def do_GET(self):
        """ Overrides the default do_GET to provide interface for geocode retrieval"""
        parsed = urlparse.urlparse(self.path)
        query = urlparse.parse_qs(parsed.query)
        if parsed.path == '/geocode/json':
            if 'address' in query:
                try:
                    geocode = gc.geocode_lookup(query['address'])
                    json_latlng = json.dumps(geocode)

                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(json_latlng)
                except:
                    self.send_error(400, "Internal Exception")
                    self.end_headers()
                    raise
            else:
                self.send_error(400, "Invalid query")
                self.end_headers()
        else:
            self.send_error(404)
            self.end_headers()


class GeoCodeServer:
    """ Starts a local server running on port 8000.
        provides methods to start and stop the server running on a separate thread.
    """

    port = 8000
    _t = None
    _running = False

    @classmethod
    def start(cls):
        """ starts the server
        """
        cls._t = threading.Thread(target=cls._run_while_true)
        cls._t.start()

    @classmethod
    def stop(cls):
        """ stops the server
        """
        cls._running = False
        print "attempting to stop server..."

        try:
            time.sleep(1)
            urllib2.urlopen("http://127.0.0.1:8000/geocode/json?address=South%Pole")
        except urllib2.URLError:
            pass

    @classmethod
    def _run_while_true(cls, server_class=BaseHTTPServer.HTTPServer, handler_class=GeoServiceHTTPReqHandler):
        """ Runs the server until _running is changed to False
        """
        server_address = ('', cls.port)

        httpd = server_class(server_address, handler_class)
        cls._running = True
        print "Server started..."
        while cls._running:
            httpd.handle_request()
        print "Server stopped"
