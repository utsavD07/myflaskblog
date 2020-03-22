from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User



class Registration(FlaskForm):
	username= StringField('Username', validators= [DataRequired(), Length(min=2,max=20)])
	email= StringField('Email', validators= [DataRequired(), Email()])
	password= PasswordField('Password', validators= [DataRequired()])
	confirm_password= PasswordField('Confirm Password', validators= [DataRequired(),EqualTo('password')])
	submit= SubmitField('Sign Up')

	def validate_username(self, username):
		user= User.query.filter_by(username=username.data).first()
		#will return the user if it already exists in the table or else will return null
		if user:
			raise ValidationError('Username already exists')

	def validate_email(self, email):
		user= User.query.filter_by(email=email.data).first()
		#will return the user if it already exists in the table or else will return null
		if user:
			raise ValidationError('Email already exists')


class Login(FlaskForm):
	email= StringField('Email', validators= [DataRequired(), Email()])
	password= PasswordField('Password', validators= [DataRequired()])
	remember= BooleanField('Remember Me')
	submit= SubmitField('Login')


class UpdateAccountForm(FlaskForm):
	username= StringField('Username', validators= [DataRequired(), Length(min=2,max=20)])
	email= StringField('Email', validators= [DataRequired(), Email()])
	picture= FileField('Update Profile Picture', validators= [FileAllowed(['jpg','jpeg','png'])])
	submit= SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username: #current_user is imported
			user= User.query.filter_by(username=username.data).first()
			#will return the user if it already exists in the table or else will return null
			if user:
				raise ValidationError('Username already exists')

	def validate_email(self, email):
		if email.data != current_user.email:
			user= User.query.filter_by(email=email.data).first()
			#will return the user if it already exists in the table or else will return null
			if user:
				raise ValidationError('Email already exists')


class RequestResetForm(FlaskForm):
	email= StringField('Email', validators=[DataRequired(), Email()])
	submit= SubmitField('Reset Password')

	def validate_email(self, email):
		user= User.query.filter_by(email=email.data).first()
		#will return the user if it already exists in the table or else will return null
		if user is None:
			raise ValidationError('Email does not exist! Register first.')


class ResetPasswordForm(FlaskForm):
	password= PasswordField('Password', validators= [DataRequired()])
	confirm_password= PasswordField('Confirm Password', validators= [DataRequired(),EqualTo('password')])
	submit= SubmitField('Reset Password')