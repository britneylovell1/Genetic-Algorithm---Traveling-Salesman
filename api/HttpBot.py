import urllib
import urllib2

class HttpBot:
    """an HttpBot represents one browser session, with cookies."""
    def __init__(self):
        cookie_handler= urllib2.HTTPCookieProcessor()
        redirect_handler= urllib2.HTTPRedirectHandler()
        self._opener = urllib2.build_opener(redirect_handler, cookie_handler)
        self._opener.addheaders = [('User-agent', 'Mozilla/5.0')] #wikipedia needs this
        self.last_headers = None

    def GET(self, url):
        response = self._opener.open(url)
        self.last_headers = response.info().headers
        return response.read()
        

    def POST(self, url, parameters):
        response = self._opener.open(url, urllib.urlencode(parameters))
        self.last_headers = response.info().headers
        return response.read()
    
    def ADD_HEADER(self, key, value):
        self._opener.addheaders = [(key, value)] #wikipedia needs this
        
