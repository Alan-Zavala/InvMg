from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError
from app.models import User, Product
from app import bcrypt

# FORMS
class LoginForm(FlaskForm):
     username = StringField(validators=[InputRequired(), Length(
          min=4, max=20)], render_kw={"placeholder": "Username"})
     
     password = PasswordField(validators=[InputRequired(), Length(
          min=4, max=20)], render_kw={"placeholder": "Password"})
     
     submit = SubmitField("Login")

class UserAddForm(FlaskForm):
     first_name = StringField(validators=[InputRequired(), Length(max=20)], render_kw={"placeholder": ""})
     last_name = StringField(validators=[InputRequired(), Length(max=20)], render_kw={"placeholder": ""})
     username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": ""})
     password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": ""})
     role = StringField(validators=[InputRequired(), Length(min=0, max=20)], render_kw={"placeholder": ""})
     submit = SubmitField("Add User")

     def validate_username(self, username):
          existing_user_username = User.query.filter_by(
               username=username.data).first()
          
          if existing_user_username:
               raise ValidationError("That username already exists")
          
# class ProductAddForm(FlaskForm):
#      name = StringField(validators=[InputRequired(), Length(max=20)], render_kw={"placeholder": ""})
#      subgenre = SelectField(u'Type', options=[('Type 1', 'Food'), ('Type 2', 'Chair')])
#      description = StringField(validators=[InputRequired(), Length(max=200)], render_kw={"placeholder": ""})
#      submit = SubmitField("Add Product")

# class OrderAddForm(FlaskForm):   # Update
#      first_name = StringField(validators=[InputRequired(), Length(max=20)], render_kw={"placeholder": ""})
#      last_name = StringField(validators=[InputRequired(), Length(max=20)], render_kw={"placeholder": ""})
#      username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": ""})
#      password = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": ""})
#      submit = SubmitField("Add Order")