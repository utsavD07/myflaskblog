from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.request import urlopen
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os
from flaskblog.config import Config

#create the extensions outside the function
db= SQLAlchemy() #an instance of sql_alchemy is created
bcrypt= Bcrypt() #an instance of bcrypt class is created
login_manager= LoginManager()

login_manager.login_view= 'users.login' #'login' is the name of the function of the route
#this is to let the login_required extension know where the login route is located

mail= Mail()


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	#initialize them within the function
	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)


	from flaskblog.posts.routes import posts
	from flaskblog.users.routes import users
	from flaskblog.main.routes import main
	from flaskblog.errors.handlers import errors

	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)
	app.register_blueprint(errors)

	return app