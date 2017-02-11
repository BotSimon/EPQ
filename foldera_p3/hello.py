from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, AnyOf, NoneOf, Optional
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_script import Manager
from flask_bootstrap import Bootstrap
import os
import os.path

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
print os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

bootstrap = Bootstrap(app)
manager = Manager(app)

#class person(db.Model):
#   __tablename__  = 'people'
#   id = db.Column(db.Integer, primary_key=True)
#   first_name = db.Column(db.String(64), unique=False)
#   last_name = db.Column(db.String(64), unique=False)
#   date_of_birth = db.Column(db.Date, unique=False)

#   books=db.relationship('book', backref='author')

#   reviews=db.relationship('review',backref='review_author')


#class book(db.Model):
#   __tablename__  = 'books'
#   id = db.Column(db.Integer, primary_key=True)
#   title = db.Column(db.String(64), unique=False)

#   author_id = db.Column(db.Integer, db.ForeignKey('people.id'))

#   description = db.Column(db.Text, unique=False)
#   year_published = db.Column(db.Date, unique=False)

#class review(db.Model):
#   __tablename__ = 'reviews'
#   id = db.Column(db.Integer, primary_key=True)

#   review_author_id = db.Column(db.Integer, db=ForeignKey('people.id'))

#   review_text = db.Column(db.Text, unique=False)
#   date_written = db.Column(db.Date, unique=False)
#   star_rating = db.Column(db.Integer, unique=False)

class Person(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(64), unique=False, nullable=False)
    first_name = db.Column(db.String(64), unique=False, nullable=False)
    #date_of_birth = db.Column(db.Date, unique=False)
    books=db.relationship('Book', backref='author')
    reviews=db.relationship('Review', backref='review_author')

class Book(db.Model):
    __tablename__ =  'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True, index=True, nullable=False)
    #description = db.Column(db.Text, unique=False)
    #year_published = db.Column(db.Date, unique=False)
    author_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    reviews=db.relationship('Review', backref='book')

class Review(db.Model):
    __tablename__ =  'reviews'
    id = db.Column(db.Integer, primary_key=True)
    review_text = db.Column(db.Text, unique=False, nullable=False)
    #date_written = db.Column(db.Date, unique=False)
    #star_rating = db.Column(db.Integer, unique=False)
    review_author_id = db.Column(db.Integer, db.ForeignKey('people.id'),nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'),nullable=False)
    #def __repr__(self):
        #found_book = Book.query.filter_by(id = self.book_id).first()
        #return '<Book title: %r>' % found_book.title


class NameForm(Form):
    nochar="_/\\:*?\"<>|"
    first_name = StringField('First name?', validators=[Required(), NoneOf(nochar)])
    last_name = StringField('Surname?', validators=[Required(), NoneOf(nochar)])
    title = StringField('Title of book reviewed', validators=[Required(), NoneOf(nochar)])
    author_first_name = StringField('Author first name', validators=[Required(), NoneOf(nochar)])
    author_surname = StringField('Author surname', validators=[Required(), NoneOf(nochar)])

    review = TextAreaField('Write a review', validators=[Required(),NoneOf(nochar)])

    submit = SubmitField('Submit')

class SearchForm(Form):
    nochar="_/\\:*?\"<>|"
    search_author = StringField('Author name?', validators=[Optional(),NoneOf(nochar)])
    search_reviewer = StringField('Reviewer name?', validators=[Optional(),NoneOf(nochar)])
    search_title = StringField('Book title?', validators=[Optional(),NoneOf(nochar)])
    submit = SubmitField('Search')


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

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit() == False:
         return render_template('search.html',
            form = form, search_active="active")
    else:
        search_author = form.search_author.data
        search_reviewer = form.search_reviewer.data
        search_title = form.search_title.data

        return render_template('search.html',
            form = form, search_active="active")


@app.route('/write', methods=['GET', 'POST'])
def write():
    form = NameForm()
    if form.validate_on_submit():
    # find or create the user
        user = Person.query.filter_by(first_name=form.first_name.data).filter_by(last_name=form.last_name.data).first()
        if user is None:
           user = Person(first_name = form.first_name.data,last_name=form.last_name.data)
           db.session.add(user)
           db.session.commit()

           session['known']=False
        else:
           session['known']=True

        session['name'] = form.first_name.data

# find or create the author

        author = Person.query.filter_by(first_name=form.author_first_name.data).filter_by(last_name = form.author_surname.data).first()
        if author is None:
           author = Person(first_name = form.author_first_name.data,last_name=form.author_surname.data)
           db.session.add(author)
           db.session.commit()

           session['known_author']=False
        else:
           session['known_author']=True

        session['author'] = form.author_first_name.data +" "+ form.author_surname.data

# find or create the Book

        book = Book.query.filter_by(title = form.title.data).first()
        if book is None:
           book = Book(title=form.title.data,author_id=author.id)

           db.session.add(book)
           db.session.commit()

           session['known_book']=False
        else:
           session['known_book']=True

        session['book'] = form.title.data

        db.session.commit()
# create the Review

        review = Review(review_text=form.review.data,book_id=book.id,review_author_id=user.id)
        db.session.add(review)
        db.session.commit()


# clear the form


        form.first_name.data = ''
        form.last_name.data = ''
        form.author_surname.data = ''
        form.author_first_name.data = ''
        form.title.data = ''
        form.review.data = ''


        flash('Your review has been submitted.')
        return render_template('write.html',
        form = form, write_active="active")
    #   old_name = session.get('name')
    #   if old_name is not None and old_name != form.name.data:
    #       flash('Looks like you have changed your name!!!!!')
    #       session['name'] = form.name.data
        #   form.name.data = ''
        #   return redirect(url_for('write'))#need a banner for this
    else:
        return render_template('write.html',
            form = form, write_active="active")

@app.route('/browse')
def browse():
    requested_review_id = request.args.get('review_id')



    #filenames=['name_title_author.txt']
    #path=fullpath('reviews')

    reviews = Review.query.all()
    display_reviews = []
    requested_id = -1
    if requested_review_id != None:
        if len(requested_review_id) > 0:
            requested_id = int(requested_review_id)

    for review in reviews:
        print(review)
        #prefix=filename.split('.',1)[0]
        #print(prefix)
        #(name,title,author)=prefix.split('_',3)
        identifier = review.id
        book =   Book.query.filter_by(id = review.book_id).first()
        book_title = book.title
        author = Person.query.filter_by(id = book.author_id).first()
        review_author = Person.query.filter_by(id = review.review_author_id).first()
        author_name = "{} {}".format(author.first_name, author.last_name)
        reviewer_name = "{} {}".format(review_author.first_name, review_author.last_name)


        display_review_text = ""
        if requested_id == review.id:
             display_review_text = review.review_text

        display_review = dict(
            id=identifier,
            author_name=author_name,
            reviewer_name=reviewer_name,
            book_title=book_title,
            review_text=display_review_text)
        display_reviews.append(display_review)

    print (display_reviews)


    return render_template('browse.html', browse_active="active", reviews=display_reviews)

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
    #manager.run()
    app.run(host='0.0.0.0', port=5005, debug=True)
