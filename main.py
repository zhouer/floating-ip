import webapp2
from google.appengine.ext import ndb

class Log(ndb.Model):
    access = ndb.DateTimeProperty(auto_now_add=True)
    path = ndb.StringProperty()
    ip = ndb.StringProperty()

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        for p in Log.query(projection=["path"], distinct=True):
            r = Log.query(Log.path == p.path).order(-Log.access).get()
            self.response.write(r.path + "\n\tIP: " +  r.ip + "\n\tAccess: " + r.access.isoformat() + "\n\n")

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
