from . import db
from datetime import datetime
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
from app import login_manager

@login_manager.user_loader
def load_user(user_id):
     return User.query.get(int(user_id))

# USERS table
class User(db.Model, UserMixin):
     id = db.Column(db.Integer, primary_key = True)
     username = db.Column(db.String(20), nullable=False, unique=True)
     password = db.Column(db.String(100), nullable=False)
     first_name = db.Column(db.String(40), nullable=False)
     last_name = db.Column(db.String(40), nullable=False)
     role = db.Column(db.String(50), nullable=False)

     def __init__(self, first_name, last_name, username, password, role):
          self.first_name = first_name
          self.last_name = last_name
          self.username = username
          self.password = generate_password_hash(password)
          self.role = role

# PRODUCTS table 
class Product(db.Model, UserMixin):
     id = db.Column(db.Integer, primary_key = True)
     name = db.Column(db.String(20), nullable=False)
     price = db.Column(db.Float, nullable=False)
     category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
     description = db.Column(db.String(200), nullable=True)

     category = db.relationship('Category', backref='product', lazy=True)

     def __init__(self, name, price, category_id, description):
          self.name = name
          self.price = price
          self.category_id = category_id
          self.description = description

# ORDERS table 
class Order(db.Model, UserMixin):
     id = db.Column(db.Integer, primary_key = True)
     order_date = db.Column(db.DateTime, default=datetime.utcnow)
     product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
     quantity = db.Column(db.Integer, nullable = False)
     total_amount = db.Column(db.Float, nullable = False)

     product = db.relationship('Product', backref='orders', lazy=True)

     def __init__(self, order_date, product_id, quantity, total_amount):
          self.order_date = order_date
          self.product_id = product_id
          self.quantity = quantity
          self.total_amount = total_amount

# INVENTORY table
class Inventory(db.Model, UserMixin):
     id = db.Column(db.Integer, primary_key=True)
     product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
     quantity = db.Column(db.Integer, nullable=False)

     product = db.relationship('Product', backref='inventory', lazy=True)

     def __init__(self, product_id, quantity):
          self.product_id = product_id
          self.quantity = quantity

# CATEGORY table
class Category(db.Model, UserMixin):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(100), nullable=False)

     def __init__(self, name):
         self.name = name