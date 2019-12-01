from flask import Flask, flash, request, redirect, url_for, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os, datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
Bootstrap(app)

db = SQLAlchemy(app)
migrate = Migrate(app,db)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app2.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140), index=True, unique=False)
    font = db.Column(db.String(64), index=True, unique=False)
    author = db.Column(db.String(64), index=True, unique=False)
    timestamp = db.Column(db.String(64), index=True, unique=False)
    def __repr__(self):
        return '<Post {}>'.format(self.content)

def add_post(content,author='',font='sans-serif',timestamp=''):
    global db
    post = Post(content=content,font=font,author=author,timestamp=timestamp)
    db.session.add(post)
    db.session.commit()

def get_posts():
    sposts = Post.query.all()
    posts = []
    for spost in sposts:
        posts.append([spost.content.split('\n'),spost.font,spost.author,spost.timestamp])
    return posts[::-1]

@app.route('/',methods=['GET','POST'])
def index():
    posts = get_posts()
    if request.method == 'POST':
        new_post = request.form['newpost']
        new_author = request.form['author']
        new_font = request.form['font']
        timestamp = datetime.date.today().strftime('%y-%m-%d')
        add_post(new_post,new_author,new_font,timestamp)
        flash('New post added successfully')
        return redirect(url_for('index'))
    return render_template('index.html',posts=posts)

@app.route('/del')
def delete():
    db.create_all()
    posts = Post.query.all()
    for p in posts:
        db.session.delete(p)
    db.session.commit()
    db.create_all()

if __name__ == '__main__':
    db.create_all()
    app.run('0.0.0.0')
