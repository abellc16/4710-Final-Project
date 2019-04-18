# example is based on http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
import os
import random
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists
from datetime import datetime
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


class Memes(db.Model):
    __tablename__ = 'memes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    up = db.Column(db.Integer)
    down = db.Column(db.Integer)
    date = db.Column(db.DateTime)
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
            if os.path.exists(app.config['UPLOAD_FOLDER']) == False:
                os.makedirs(app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            newimage = Memes(id = db.session.query(Memes).count() + 1, name = file.filename, up = 0, down = 0, date = datetime.now())
            db.session.add_all([newimage])
            db.session.commit()
            path = 'http://127.0.0.1:5000/dankmemes/' + file.filename
            return render_template('homepage.html', image_file = path, ups = 0, downs = 0)
    elif request.method == 'GET':
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            db.drop_all()
            db.create_all()
            memelist = os.listdir(app.config['UPLOAD_FOLDER'])
            index = 0
            for x in range(len(memelist)):
                image = Memes(id = x, name = memelist[x], up = 0, down = 0, date = datetime.now())
                index += 1
                db.session.add(image)
            db.session.commit()
        rand = random.randrange(0, db.session.query(Memes).count())
        row = db.session.query(Memes)[rand]
        path = 'http://127.0.0.1:5000/dankmemes/' + row.name
        return render_template('homepage.html', image_file = path, ups = row.up, downs = row.down, date = row.date)

@app.route('/dankmemes/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/dankmemes/<filename>/up', methods=['POST'])
def send_up(filename):
    meme=Memes.query.filter_by(name=filename).first()
    meme.up += 1
    db.session.commit()
    path = 'http://127.0.0.1:5000/dankmemes/' + filename
    return render_template('homepage.html', image_file = path, ups = meme.up, downs = meme.down, date = meme.date)

@app.route('/dankmemes/<filename>/down', methods=['POST'])
def send_down(filename):
    meme=Memes.query.filter_by(name=filename).first()
    meme.down += 1
    db.session.commit()
    path = 'http://127.0.0.1:5000/dankmemes/' + filename
    return render_template('homepage.html', image_file = path, ups = meme.up, downs = meme.down, date = meme.date)

if __name__ == '__main__':
    app.debug = True
    ip = '127.0.0.1'
    app.run(host=ip)