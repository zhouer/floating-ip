import datetime
import webapp2
from google.appengine.ext import ndb

class Log(ndb.Model):
    access = ndb.DateTimeProperty(auto_now_add=True)
    path = ndb.StringProperty()
    ip = ndb.StringProperty()

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        now = datetime.datetime.now()
        for p in Log.query(projection=["path"], distinct=True):
            r = Log.query(Log.path == p.path).order(-Log.access).get()
            diff = (now - r.access).seconds
            self.response.write('%s\n\tIP: %s\n\tUpdate: %d seconds ago\n\n' % (r.path, r.ip, diff))

class LogPage(webapp2.RequestHandler):
    def get(self, path):
        if path == 'favicon.ico':
            return

        log = Log()
        log.path = path
        log.ip = self.request.remote_addr
        log.put()

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Access %s from %s' % (path, self.request.remote_addr))

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/(.*)', LogPage),
], debug=True)
