import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail



def save_picture(form_picture):
	random_hex= secrets.token_hex(8)
	_, f_ext= os.path.split(form_picture.filename)
	picture_fn= random_hex + f_ext
	picture_path= os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
	output_size= (125,125) #size of the output image
	i= Image.open(form_picture)
	i.thumbnail(output_size) #resize the image so that it takes less time to load

	i.save(picture_path)

	return picture_fn



def send_reset_email(user):
	token= user.get_reset_token()
	msg= Message('Password Reset Request', sender='utsavdas1998@gmail.com', recipients=[user.email])
	msg.body= f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email.
'''									#_external= True so that absolute urls are displayed (and not relative)
	mail.send(msg)