import os
from flask import Flask, render_template, session, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from sqlalchemy.sql import text
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder='templates')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
     return User.query.get(int(user_id))

def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        session.execute(table.delete())
    session.commit()

class User(db.Model, UserMixin):
     id = db.Column(db.Integer, primary_key = True)
     username = db.Column(db.String(40), nullable=False, unique=True)
     password = db.Column(db.String(40), nullable=False)

class RegisterForm(FlaskForm):
     username = StringField(validators=[InputRequired(), Length(
          min=4, max=20)], render_kw={"placeholder": "Username"})
     
     password = PasswordField(validators=[InputRequired(), Length(
          min=4, max=20)], render_kw={"placeholder": "Password"})
     
     submit = SubmitField("Register")

     def validate_username(self, username):
          existing_user_username = User.query.filter_by(
               username=username.data).first()
          
          if existing_user_username:
               raise ValidationError(
                    "That username already exists"
               )

class LoginForm(FlaskForm):
     username = StringField(validators=[InputRequired(), Length(
          min=4, max=20)], render_kw={"placeholder": "Username"})
     
     password = StringField(validators=[InputRequired(), Length(
          min=4, max=20)], render_kw={"placeholder": "Password"})
     
     submit = SubmitField("Login")

@app.route('/test')
def testdb():
    try:
        users = db.session.execute(db.select(User)
            .order_by(User.username)).scalars()

        user_text = '<ul>'
        for name in users:
            user_text += '<li>' + name.username + '</li>'
        user_text += '</ul>'
        return user_text
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
    
@app.route('/')
def home():
     return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
     form = LoginForm()
     if form.validate_on_submit():
          user = User.query.filter_by(username=form.username.data).first()
          if user:
               if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for('dashboard'))
     return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
     return render_template('dashboard.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
     logout_user()
     return redirect(url_for('login'))

#   ------ unnecessary function ------
#
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#      form = RegisterForm
     
#      if form.validate_on_submit():
#           hashed_password = bcrypt.generate_passowrd_hash(form.passowrd.data)
#           new_user = User(username=form.username.data, password=hashed_password)
#           db.session.add(new_user)
#           db.session.commit()
#           return redirect(url_for('login'))
     
#      return render_template('register.html', form=form)


if __name__ == '__main__':
     app.run(debug=True)

