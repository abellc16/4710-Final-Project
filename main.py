# example is based on http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
import os
import random
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import jinja2
import util

# get current app directory
dir_path = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = dir_path + '/dankmemes/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir_path, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# The db object instantiated from the class SQLAlchemy represents the database and
# provides access to all the functionality of Flask-SQLAlchemy.
db = SQLAlchemy(app)

class Meme(db.Model):
	__tablename__ = 'memes'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, unique=True)
	up = db.Column(db.Integer)
	down = db.Column(db.Integer)
	def __repr__(self):
		return '<Memes %r>' % self.name

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		if 'file' not in request.files:
			log = 'no file field in request.'
			return render_template('homepage.html', log = log)
		file = request.files['file']
		if file.filename == '':
			log = 'Empty filename.'
			return render_template('homepage.html', log = log)
		if file and util.allowed_file(file.filename):
			filename = secure_filename(file.filename)
			if os.path.exists(app.config['UPLOAD_FOLDER']) == False:
				os.makedirs(app.config['UPLOAD_FOLDER'])
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return render_template('homepage.html', filename=filename, column_names=column_names, data_part=data_part)
	elif request.method == 'GET':
		return render_template('homepage.html')

@app.route('/')
def index():
	db.drop_all()
	db.create_all()
	image1 = Memes(id = 1, name = '1.jpg', up = 0, down = 0)
	image2 = Memes(id = 2, name = '2.jpg', up = 0, down = 0)
	image3 = Memes(id = 3, name = '3.jpg', up = 0, down = 0)
	image4 = Memes(id = 4, name = '4.jpg', up = 0, down = 0)
	image5 = Memes(id = 5, name = '5.jpg', up = 0, down = 0)
	image6 = Memes(id = 6, name = '6.jpg', up = 0, down = 0)
	image7 = Memes(id = 7, name = '7.jpg', up = 0, down = 0)
	image8 = Memes(id = 8, name = '8.jpg', up = 0, down = 0)
	image9 = Memes(id = 9, name = '9.jpg', up = 0, down = 0)
	image10 = Memes(id = 10, name = '10.jpg', up = 0, down = 0)
	image11 = Memes(id = 11, name = '11.jpg', up = 0, down = 0)
	image12 = Memes(id = 12, name = '12.jpg', up = 0, down = 0)
	image13 = Memes(id = 13, name = '13.jpg', up = 0, down = 0)
	image14 = Memes(id = 14, name = '14.jpg', up = 0, down = 0)
	image15 = Memes(id = 15, name = '15.jpg', up = 0, down = 0)
	db.session.add_all([image1, image2, image3, image4, image5, image6, image7, image8, image9, image10,
	                    image11, image12, image13, image14, image15])
	db.session.commit()

@app.route('/')
def getRandom():
    rand = random.randrange(0, db.session.query(Memes).count())
    row = db.session.query(Memes)[rand]
    path = os.path.join(app.config['UPLOAD_FOLDER'], row.name)
    return render_template('homepage.html', image_file = path)
    print path

if __name__ == '__main__':
	app.debug = True
	ip = '127.0.0.1'
	app.run(host=ip)

