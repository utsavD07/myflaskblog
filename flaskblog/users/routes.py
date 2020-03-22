from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (Registration, Login, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

users= Blueprint('users', __name__) #'users' is the name of the blueprint

@users.route('/register', methods=['GET','POST'])
def register():
	if current_user.is_authenticated: #to check if user is logged-in already
		return redirect(url_for('main.home'))

	form= Registration()

	if form.validate_on_submit():
		hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user= User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		#we will modify the layout.html so that flash messages are displayed on every page
		flash('Registered successfully for {}!'.format(form.username.data),'success') #success is the name of the bootstrap class
		return redirect(url_for('users.login'))#home is the name of the function and not the route

	return render_template('register.html',title='Register',form=form)



@users.route('/login', methods=['GET','POST'])
def login():
	if current_user.is_authenticated: #to check if user is logged in already
		return redirect(url_for('main.home'))

	form= Login()

	if form.validate_on_submit():
		user= User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data) #funtion imported from flask_login
			next_page= request.args.get('next') #it'll return the 'next' query i.e the next route if it exists or else it will return none(i.e null)
			#args is a dict but still don't use [] to access the 'next' query because it will throw an error if 'next' doesn't exist and .get() will only return none
			
			if next_page: #if next_page is not none
				return redirect(next_page)

			else:
				return redirect(url_for('main.home'))

		else:
			flash('Login Unsuccessful. Please check credentials!','danger')

	return render_template('login.html',title='Login',form=form)


@users.route('/logout')
def logout(): #no argument because it already knows which user is logged-in
	logout_user()
	return redirect(url_for('main.home'))



#if we try to access the account route manually, we will be redirected to the login page by the login_user extension
@users.route('/account', methods=['GET','POST'])
@login_required #now the extension knows that we need to login before accessing the account route
#but we also need to tell the extension where the login route is located so it is done in the __init__.py file
def account():
	form= UpdateAccountForm()
	if form.validate_on_submit(): #if form is valid, update the info
		if form.picture.data:
			picture_file= save_picture(form.picture.data)
			current_user.image= picture_file

		current_user.username= form.username.data
		current_user.email= form.email.data
		db.session.commit()
		flash('Your account info has been updated!', 'success')
		return redirect(url_for('users.account'))

	image_file= url_for('static', filename='profile_pics/' + current_user.image)
	return render_template('account.html',title='Account', image_file=image_file, form=form)



@users.route('/user/<string:username>')
def user_posts(username):
	page= request.args.get('page', 1, type=int)
	user= User.query.filter_by(username=username).first_or_404()
	#returns 404 if none or the first user with that username

	posts= Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template('user_posts.html', posts=posts, user=user)



@users.route('/reset_password', methods=['GET','POST'])
def reset_request():
	if current_user.is_authenticated: #user has to be logged out to reset password
		return redirect(url_for('main.home'))

	form= RequestResetForm()
	if form.validate_on_submit():
		user= User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent to reset your password', 'info')
		return redirect(url_for('users.login'))
	return render_template('reset_request.html', title='Reset Password', form=form)



@users.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
	if current_user.is_authenticated: #user has to be logged out to reset password
		return redirect(url_for('main.home'))

	user= User.verify_reset_token(token)
	if user is None: #if the token is invalid or has expired
		flash('Token invalid or expired!', 'warning')
		return redirect(url_for('users.reset_request'))

	#if the token is valid and on time
	form= ResetPasswordForm()
	if form.validate_on_submit():

		hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password= hashed_password
		db.session.commit()
		flash('Password changed successfully','success') #success is the name of the bootstrap class
		return redirect(url_for('users.login'))#home is the name of the function and not the route

	return render_template('reset_token.html', title='Reset Password', form=form)