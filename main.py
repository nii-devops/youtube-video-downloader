
from pytube import YouTube
import os
from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
# Import your forms from the forms.py
from forms import RegisterForm, LoginForm, URLForm, ContactForm

from time import sleep
from typing import List
from datetime import datetime
import pathlib
import smtplib

# Import dotenv
from dotenv import load_dotenv

load_dotenv('.env')


# SMTP CREDENTIALS
gmail_smtp = ("smtp.gmail.com")
port = 587

my_email = os.getenv('MY_EMAIL')
email_password = os.getenv('EMAIL_PASSWORD')



app = Flask(__name__)
# app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

ckeditor = CKEditor(app)
Bootstrap5(app)


# Create a user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None)


#######################
### DATABASE MODELS ###
########################

# Create User DB Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # Create a relationship between User table and Downloaded File table
    downloaded_files = db.relationship('DownloadedFile', backref='user', lazy='dynamic')

    # Create a relationship between User table and Downloaded File table
    messages = db.relationship('Message', backref='user', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.f_name}', '{self.l_name}', '{self.email}')"


NOW = datetime.today().replace(microsecond=0)

class DownloadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=NOW)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    message = db.Column(db.String(1500), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


with app.app_context():
    db.create_all()


##########################
#<-----   ROUTES   ----->#
###########################

@app.route('/', methods=['get', 'post'])
def home():
    form = URLForm()
    if form.validate_on_submit():
        DOWNLOAD_FOLDER = (pathlib.Path.home()/"Downloads")
        url = form.url.data
        try:
            # Create YouTube object
            yt = YouTube(url)

            # Get the highest resolution stream available
            stream = yt.streams.get_highest_resolution()

            # Download the video
            stream.download(output_path=DOWNLOAD_FOLDER)
            flash(f"Downloaded '{yt.title}' successfully!", category='success')
            
            return redirect(url_for('home'))
        
        except Exception as err:
            flash(f"An error occurred {err}!", category='danger')

    return render_template('index.html', title='Home', form=form)



@app.route('/about-us')
def about():
    return render_template('about.html', title='About')


@app.route('/contact-us', methods=['get', 'post'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        title = form.title.data
        msge = form.message.data
        message = msge.replace('<p>',"").replace('</p>',"").replace('<br>',"").replace('</br>',"").replace('<br/>',"")

        #Add message to DB
        new_message = Message(
            name=name,
            email=email,
            title=title,
            message=message
        )
        db.session.add(new_message)
        db.session.commit()

        with smtplib.SMTP(gmail_smtp, port) as connection:
            connection.starttls()
            connection.login(user=my_email, password=email_password)
            connection.sendmail(from_addr=my_email,
                            to_addrs=email,
                            msg=f"Subject:Re: Enquiry Response for {title}"
                                f"\n\nHello {name}, \nWe have received your enquiry/message. \nOur staff will review and revert shortly.\nRegards... \n\nYT-DL Team")
        return redirect(url_for('home'))
    return render_template('contact.html', title='Contact Us', form=form)


if __name__ == "__main__":
    app.run(debug=True)





