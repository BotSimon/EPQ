from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
app = Flask(__name__)
app.config['SECRET_KEY'] = 'banana'
bootstrap = Bootstrap(app)
import os
import os.path
 
manager = Manager(app) 

class NameForm(Form):
	name = StringField('What is your name?', validators=[Required()])
	review = TextAreaField('Write a review', validators=[Required()])
	author = StringField('Name of author', validators=[Required()])
	title = StringField('Title of book reviewed', validators=[Required()])
	submit = SubmitField('Submit')

def writetofile (name, review, author, title):
	text="name:  {}, \nreview: {}, \nauthor: {}, \ntitle: {}".format(name, review, author, title)
	save_path = 'Desktop/foldera/reviews'
	filename="{}_{}_{}".format(author, title, name)
	completename = os.path.join(save_path, filename+".txt")
	file1 = open(completename, "w")
	file1.write(text)
	file1.close()	



	#with open (filename, "wb") as fo:
		#fo.write(text)

@app.route('/')
def home():
	return render_template('index.html', home_active="active")

@app.route('/search')
def select():
	return render_template('user.html', search_active="active")
	
@app.route('/write', methods=['GET', 'POST'])
def write():	
 	form = NameForm()
	if form.validate_on_submit():
		name = form.name.data
		review = form.review.data
		author = form.author.data
		title = form.title.data
		writetofile(name, review, author, title)	
	 	
	#	old_name = session.get('name')
	#	if old_name is not None and old_name != form.name.data:
	#		flash('Looks like you have changed your name!!!!!') 
	#		session['name'] = form.name.data
		#	form.name.data = ''
		#	return redirect(url_for('write'))#need a banner for this
	
	return render_template('write.html', 
		form = form, write_active="active")
 
@app.route('/read')
def read():
	return render_template('base.html', read_active="active")

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')


@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html')

if __name__ == '__main__':
	manager.run() 
	app.run(debug=True)
