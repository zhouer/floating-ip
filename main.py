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
            latest = Log.query(Log.path == p.path).order(-Log.access).get()
            self.response.write('%s\n\tIP: %s\n\tUpdate: %s\n\n' % (latest.path, latest.ip, latest.access))


class LogPage(webapp2.RequestHandler):
    def get(self, path):
        now = datetime.datetime.now()
        latest = Log.query(Log.path == path).order(-Log.access).get()

        self.response.headers['Content-Type'] = 'text/plain'
        if latest:
            self.response.write(latest.ip)
        else:
            self.response.write('No IP records')

    def post(self, path):
        log = Log()
        log.path = path
        log.ip = self.request.remote_addr
        log.put()

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Access %s from %s' % (path, self.request.remote_addr))

    def delete(self, path):
        keys = Log.query(Log.path == path).iter(keys_only=True)
        ndb.delete_multi(keys)

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Remove all records of %s' % (path))


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/(.*)', LogPage),
], debug=True)
