from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, AnyOf, NoneOf
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
import os
import os.path
app = Flask(__name__)
bootstrap = Bootstrap(app)
manager = Manager(app) 

class NameForm(Form):
	nochar="_/\\:*?\"<>|"
	name = StringField('What is your name?', validators=[Required(), NoneOf(nochar)])
	review = TextAreaField('Write a review', validators=[Required()])
	author = StringField('Name of author', validators=[Required(), NoneOf(nochar)])
	title = StringField('Title of book reviewed', validators=[Required(), NoneOf(nochar)])
	submit = SubmitField('Submit')

def writetofile (name, review, author, title):
	text="name:  {}, \nreview: {}, \nauthor: {}, \ntitle: {}".format(name, review, author, title)
	save_path = fullpath('reviews')
	filename="{}_{}_{}".format(author, title, name)
	completename = os.path.join(save_path, filename+".txt")
	file1 = open(completename, "w")
	file1.write(text)
	file1.close()	

def fullpath (path): 
	absolutepath = os.path.abspath(path)
	return(absolutepath)






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
		flash('Your review has been submitted.')	
		return render_template('write.html',
			form = form, write_active="active") 	
	#	old_name = session.get('name')
	#	if old_name is not None and old_name != form.name.data:
	#		flash('Looks like you have changed your name!!!!!') 
	#		session['name'] = form.name.data
		#	form.name.data = ''
		#	return redirect(url_for('write'))#need a banner for this
	else:
		return render_template('write.html', 
			form = form, write_active="active")
 
@app.route('/browse')
def browse():

	filenames=['name_title_author.txt']
	path=fullpath('reviews')
	for filename in os.listdir(path):
		print(filename)	
		filenames.append(filename)
	reviews=[]
	for filename in filenames:
		print(filename)
		prefix=filename.split('.',1)[0]
		print(prefix)
		(name,title,author)=prefix.split('_',3)

	
		displayname="{} {} {}".format(title, author, name)
		url="read/{}".format(filename)
		review={'url':url, 'displayname': displayname}
		print(review)
		reviews.append(review)
	return render_template('browse.html', browse_active="active", reviews=reviews)

@app.route('/read/<filename>')
def read(filename):
	prefix=filename.split('.',1)[0]
	(name,title,author)=prefix.split('_',3)
	read_path = fullpath('reviews')
	completename = os.path.join(read_path, filename)
	file1 = open(completename, "r")
	review=file1.read()
	file1.close()	

	return render_template('read.html', review=review, name=name, author=author)
	


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')


@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html')

if __name__ == '__main__':
	manager.run() 
	app.run(debug=True)
