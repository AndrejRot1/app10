import os
import cgi
import urllib
import datetime
from google.appengine.api import users
import pkg_resources
from webapp2_extras import jinja2
from jinja2 import Environment, PackageLoader
import webapp2
from google.appengine.ext.webapp.util import login_required




# from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2




views_dir = os.path.join(os.path.dirname(__file__), 'views')

#jinja_environment = Environment(autoescape=True,
#loader=PackageLoader(views_dir, 'views'))


env = Environment(
    loader=PackageLoader('app10', 'views')
    
)



class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)


class Prevozi(ndb.Model):
    user_id = ndb.StringProperty()
    email = ndb.StringProperty(indexed=True)
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


class Logout(Handler):
    def get(self):
        logout_url = users.create_logout_url('/')


class Index(Handler):


     def _render(self,template,**value):
        template = env.get_template('index.html')
        j = jinja2.get_jinja2()
        html = j.render_template(template,**value)
        self.response.write(html)

     def get(self):
        logout_url = users.create_logout_url('/')
        self._render('index.html',logout_url = logout_url)
      



class Login(Handler):
  
    def get(self):
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
        self.render('post2.html')
      
    def post(self):
		self.render('post2.html')
       
		form_input = Prevozi(start = self.request.get('field1'),
							 stop = self.request.get('field2'),
							 telefon = self.request.get('field3'),
                             prispevek = self.request.get('field4'),
							 date = self.request.get('field5'),
                             time = self.request.get('field6'),
                             email = users.get_current_user().email(),
                             user_id = users.get_current_user().user_id())
                            

		form_input_key = form_input.put()

	
class Retrive(Handler):
    def _render(self,template,**value):
        j = jinja2.get_jinja2()
        html = j.render_template(template,**value)
        self.response.write(html)
 

    def get(self):
        logout_url = users.create_logout_url('/')
        messg = Prevozi.query().fetch(100)
        self._render('retrive.html',logout_url = logout_url)

    def post(self):
        mesto1 = self.request.get('start')
        mesto2 = self.request.get('stop')
        messg = Prevozi.query(Prevozi.start == mesto1, Prevozi.stop == mesto2)
        self._render('look.html',messg = messg)

class Posts(Handler):

     def _render(self,template,**value):
        j = jinja2.get_jinja2()
        html = j.render_template(template,**value)
        self.response.write(html)

 
     def get(self):
        user =  users.get_current_user().user_id()
        logout_url = users.create_logout_url('/')
        messg = Prevozi.query(Prevozi.user_id == user)
        self._render('my-posts.html',messg = messg,logout_url = logout_url)

     def post(self):
         user =  users.get_current_user().user_id()
         logout_url = users.create_logout_url('/')
         field2 = self.request.get('field2')
         field1 = self.request.get('field2')
         messg = Prevozi.query(Prevozi.user_id == user)


      #   prispevek = Prevozi.query(Prevozi.prispevek == '4').fetch(1)[0]
       #  ime = prispevek.key.id()
        # ndb.Key(Prevozi, int(ime)).delete()
       
       # Majhen trik kako dobiti vrednost polja

         if field1 == field2:
             ndb.Key(Prevozi, int(field2)).delete()
            # key = ndb.key(Prevozi,int(id)).delete()
             
         else:
            ime = field1

         messg = Prevozi.query(Prevozi.user_id == user)
         self._render('my-posts.html',messg = messg,logout_url = logout_url)

            

        

app = webapp2.WSGIApplication([  
    ('/',Index),
    ('/post',Post),
    ('/retrive',Retrive),
    ('/myposts',Posts),
    ('/Logout',Logout),
], debug=True)

