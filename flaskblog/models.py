from flask import current_app
from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin #the decorator function used below requires 4 attributes from the model to function. The UserMixin class provides this by default
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



#decorator function to let the login_manager know which user to fetch and return from the table
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	name_id= db.Column(db.Integer,primary_key=True)
	username= db.Column(db.String(20), nullable=False, unique=True)
	email= db.Column(db.String(120), nullable=False, unique=True)
	image= db.Column(db.String(20), nullable=False, default='default.jpg')
	password= db.Column(db.String(60), nullable=False)
	posts= db.relationship('Post', backref='author', lazy=True)

	def __repr__(self):
		return f"User('{self.username}' , '{self.email}' , '{self.image}')"

	def get_id(self):
		return (self.name_id)

	def get_reset_token(self, expires_sec=1800):
		s= Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.name_id}).decode('utf-8')

	@staticmethod #to let the class method know not to expect the 'self' instance
	def verify_reset_token(token):
		s= Serializer(current_app.config['SECRET_KEY'])
		#the token can be invalid or get expired so put it in a try-except block
		try:
			user_id= s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)



class Post(db.Model):
	name_id= db.Column(db.Integer, primary_key=True)
	title= db.Column(db.String(100), nullable=False)
	date_posted= db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content= db.Column(db.Text, nullable=False)
	user_id= db.Column(db.Integer, db.ForeignKey('user.name_id'), nullable=False)

	def __repr__(self):
		return f"Post({self.title} , {self.date_posted})"