from datetime import datetime, timezone
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '039b709a4245bf9b4e829c49981dd5bd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app) # membuat instace db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self): 
        return f"User('{self.username}','{self.email}','{self.image_file}')"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"


posts = [
    {
        'author': 'Jamal',
        'title': 'Tutorial Memakan Tulang Ikan',
        'content': 'Pertama, jangan terburu-buru. Tulang ikan terdiri dari dua bagian. Satu keras, kedua lembut.',
        'date_posted': 'Oct 14th, 2024'
    },
    {
        'author': 'Juminten',
        'title': 'Cara melompat dengan baik',
        'content': 'Jika Anda berada di plafon dapur, jangan langsung loncat ke lantai. Tapi carilah sesuatu yang menggantung di dinding.',
        'date_posted': 'Oct 14th, 2024'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html", title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data:
            pass
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)