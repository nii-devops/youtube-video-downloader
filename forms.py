
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, TextAreaField, SelectField, URLField, FileField
from wtforms.validators import DataRequired, URL, EqualTo, Length
from flask_ckeditor import CKEditorField


class RegisterForm(FlaskForm):
    f_name      = StringField(label='First name(s)', validators=[DataRequired()])
    l_name      = StringField(label='Last name', validators=[DataRequired()])
    email       = EmailField(label='Email', validators=[DataRequired()])
    password    = PasswordField(label='Password', validators=[Length(min=8), DataRequired(),
                                EqualTo('password_2', message='Passwords must match')])
    password_2  = PasswordField(label='Repeat Password', validators=[DataRequired()])
    submit      = SubmitField("Register")


class LoginForm(FlaskForm):
    email       = EmailField(label='Email', validators=[DataRequired()])
    password    = PasswordField(label='Password', validators=[DataRequired()], render_kw={"placeholder":"Paste YouTube Video URL Here..."})
    submit      = SubmitField("Download")


# Form to Download YouTube Video
class URLForm(FlaskForm):
    #file = FileField('Download Folder', validators=[DataRequired()], render_kw={'placeholder':'Select Download Folder'})
    url    = URLField("YouTube Video URL", validators=[DataRequired(), URL()], render_kw={'placeholder':'Paste YouTube Video URL Here'})
    submit  = SubmitField("Download Video")


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField('Email Address', validators=[DataRequired()])
    title = StringField("Message Topic", validators=[DataRequired()])
    message = CKEditorField('Message', validators=[DataRequired()])
    submit  = SubmitField("Send")


