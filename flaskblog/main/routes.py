from flask import render_template, request, Blueprint
from flaskblog.models import Post

main= Blueprint('main', __name__) #'main' is the name of the blueprint

@main.route('/')
@main.route('/home')
def home():
	page= request.args.get('page', 1, type=int) #query parameter
					#page parameter	#default page number=1 #type checks that only integers are passed for page numbers
	posts= Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template('home.html', posts=posts)



@main.route('/about')
@main.route('/aboutpage')
def about():
	return render_template('about.html',title='About Page')
