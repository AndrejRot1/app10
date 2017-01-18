import os
import cgi
import urllib
import datetime
from google.appengine.api import users
from webapp2_extras import jinja2


# from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2




views_dir = os.path.join(os.path.dirname(__file__), 'views')



class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)


class Prevozi(ndb.Model):
    email = ndb.StringProperty(indexed=False)
    message_time = ndb.DateTimeProperty(auto_now_add = True)
    start = ndb.StringProperty()
    stop = ndb.StringProperty()
    telefon = ndb.StringProperty()
    prispevek = ndb.StringProperty()
    date = ndb.StringProperty()
    time = ndb.StringProperty()



class Handler(webapp2.RequestHandler):

    def render(self, filename):
        f = open(views_dir + '/' + filename)
        self.response.write(f.read())
        f.close()


class Index(Handler):

     def get(self):
        self.render('index.html')

        user = users.get_current_user()
        
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
                nickname, logout_url)
        else:
            login_url = users.create_login_url('/')
            greeting = '<a href="{}">Sign in</a>'.format(login_url)

        self.response.write(
            '<html><body>{}</body></html>'.format(greeting))
 
       
        
class Post(Handler):
	def get(self):
		self.render('post.html')

	def post(self):
		self.render('post.html')
       
		form_input = Prevozi(start = self.request.get('field1'),
							 stop = self.request.get('field2'),
							 telefon = self.request.get('field3'),
                             prispevek = self.request.get('field4'),
							 date = self.request.get('field5'),
                             time = self.request.get('field6'),
                             email = users.get_current_user().email())
                            

		form_input_key = form_input.put()

       

        

	
class Retrive(Handler):
    def _render(self,template,**value):
        j = jinja2.get_jinja2()
        html = j.render_template(template,**value)
        self.response.write(html) 

    def get(self):
        messg = Prevozi.query().fetch(100)
        self._render('retrive.html',messg = messg)



app = webapp2.WSGIApplication([  
    ('/',Index),
    ('/post',Post),
    ('/retrive',Retrive),
], debug=True)

