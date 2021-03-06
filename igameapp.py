import os
import cgi
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.db import GqlQuery

class GameData(db.Model):
#    author = db.UserProperty()
#    url = db.StringProperty()
#    disc = db.StringProperty(multiline=True)
#    date = db.DateTimeProperty(auto_now_add=True)
    name = db.StringProperty()
    width = db.IntegerProperty()
    height = db.IntegerProperty()
    category = db.ReferenceProperty()
    dir = db.StringProperty()
    
class Category(db.Model):
    name = db.StringProperty()
    count = db.IntegerProperty()

  
class MainPage(webapp.RequestHandler):
    def get(self):
 #       game = GameData()
  #      game.name = 'kuanggong'
  #      game.width = 550
  #      game.height = 400
  #      game.put()

        
#        user = users.get_current_user()

#        dataList = ZzData.gql('')
#        data = db.GqlQuery('SELECT * FROM Greeting ORDER BY date DESC LIMIT 10')
#        zzList = []
#        for data in dataList:
#            if greeting.author:
#                name = greeting.author.nickname()
#            else:
#                name = 'An anonymous person'
#            content = cgi.escape(greeting.content)
#            zzList.append({'url': data.url, 'disc': cgi.escape(data.disc)})
        game_list = GameData.all()
        category_list = Category.all()
        template_values = {
            'game_list': game_list,
            'category_list': category_list,
#            'user': user,
#            'zzList': zzList,
        }
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
        
class GamePlay(webapp.RequestHandler):
    def get(self):
        #query = GqlQuery('SELECT __key__ FROM GameData WHERE name = :1', 'kuanggong')
        #a = query.get()
        key = self.request.get('key')
        game = GameData.get(key)
        category_list = Category.all()
        template_values = {
            'game': game,
            'category_list': category_list,
            }
        path = os.path.join(os.path.dirname(__file__), 'gameplay.html')
        self.response.out.write(template.render(path, template_values))           
#class Submit(webapp.RequestHandler):
#    def post(self):
#        data = ZzData()

#        if users.get_current_user():
#            greeting.author = users.get_current_user()

#        data.url = self.request.get('zzUrl')
#        data.disc = self.request.get('zzDisc')
#        data.put()
#        self.redirect('/')

#        path = os.path.join(os.path.dirname(__file__), 'sign.html')
#        content = cgi.escape(self.request.get('content'))
#        template_values = {
#            'content': content,
#        }
#        self.response.out.write(template.render(path, template_values))

#class Userlogin(webapp.RequestHandler):
#    def get(self):
#        self.redirect(users.create_login_url('/'))

class GameList(webapp.RequestHandler):
    def get(self):
        #query = GqlQuery('SELECT __key__ FROM GameData WHERE name = :1', 'kuanggong')
        #a = query.get()
        #key = self.request.get('key')
        #game = GameData.get(key)
        key = self.request.get('key')
        category = Category.get(key)
        #query = GqlQuery('SELECT __key__ FROM Category WHERE name = :1', '')
        game_list = GameData.gql('WHERE category = :1', category)
        category_list = Category.all()
        template_values = {
            'category': category,
            'game_list': game_list,
            'category_list': category_list,
            }
        path = os.path.join(os.path.dirname(__file__), 'gamelist.html')
        self.response.out.write(template.render(path, template_values))           

        
class AddGame(webapp.RequestHandler):
    def get(self):
        game_list = GameData.all()
        category_list = Category.all()
        #query = GqlQuery('SELECT __key__ FROM Category WHERE name = :1', '')
        #cat = category_list.get()
        #print cat.count
        #for item in game_list:
        #    item.category = cat
        #    item.save()
        #    item.category.count += 1
        #    item.category.save()
        #    if category_list.name == '432':
        #        item.delete()
            
        path = os.path.join(os.path.dirname(__file__), 'addgame.html')
        self.response.out.write(template.render(path, {'game_list': game_list, 'category_list': category_list,}))
    def post(self):
        if self.request.get('gameName'):
            data = GameData()
            data.name = self.request.get('gameName')
            data.width = int(self.request.get('gameWidth'))
            data.height = int(self.request.get('gameHeight'))
            data.category = Category.get(self.request.get('gameCategory'))
            data.put()
        if self.request.get('category'):
            data = Category()
            data.name = self.request.get('category')
            data.put()
        self.redirect(users.create_login_url('/addgame'))    

class gigapp(webapp.RequestHandler):
    def get(self):
        template_values = {
            'user': 'please post',
            }
        path = os.path.join(os.path.dirname(__file__), 'gigapp.html')
        self.response.out.write(template.render(path, template_values))
    def post(self):
        user = self.request.get('gacall_useremail');
        template_values = {
            'user': user,
            }
        path = os.path.join(os.path.dirname(__file__), 'gigapp.html')
        self.response.out.write(template.render(path, template_values))
        
        

application = webapp.WSGIApplication([
                                    ('/', MainPage),
                                    ('/gameplay', GamePlay),
                                    ('/gamelist', GameList),
                                    ('/addgame', AddGame),
#                                    ('/submit', Submit),
#                                    ('/login', Userlogin),
                                    ('/gigapp', gigapp),
                                    ],
                                    debug=True)

def main():
    run_wsgi_app(application)

if __name__ =='__main__':
    main()