from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='templates')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
     return User.query.get(int(user_id))

# def clear_data(session):
#     meta = db.metadata
#     for table in reversed(meta.sorted_tables):
#         session.execute(table.delete())
#     session.commit()

class User(db.Model, UserMixin):
     id = db.Column(db.Integer, primary_key = True)
     username = db.Column(db.String(20), nullable=False, unique=True)
     password = db.Column(db.String(80), nullable=False)

     def __init__(self, username, password):
          self.usename = username
          self.password = bcrypt.generate_password_hash(password)

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
            user_text += '<li>' + name.username + ',' + name.password + '</li>'
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
               if check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for('dashboard'))
          else:
               flash('Invalid username or password', 'error')
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

if __name__ == '__main__':
     app.run(debug=True)

