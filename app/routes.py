from flask import render_template, session, request, redirect, url_for, flash, current_app as app
from app import db, bcrypt
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import generate_password_hash, check_password_hash
from app.forms import UserAddForm, ProductAddForm, OrderAddForm, LoginForm
from app.models import User, Product, Order, Inventory, Category


# def clear_data(session):
#     meta = db.metadata
#     for table in reversed(meta.sorted_tables):
#         session.execute(table.delete())
#     session.commit()


# -------------------------------------------------------- ROUTES --------------------------------------------------------------


# test database
@app.route('/test')
def testdb():
     try:
          users = db.session.execute(db.select(User)
               .order_by(User.username)).scalars()
          # products = db.session.execute(db.select(Product) # update
          #      .order_by(User.name)).scalars()
          # orders = db.session.execute(db.select(Order)   # update
          #      .order_by(User.username)).scalars()
     
          # all_text = '<ul>'
          # for name in users:
          #      all_text += '<li>' + name.username + ', ' + name.password + '</li>'
          # all_text += '</ul>'

          # all_text = '<ul>'
          # for product in products:
          #      all_text += '<li>' + product.name + ',' + product.description + '</li>'
          # all_text += '</ul>'

          # all_text = '<ul>'
          # for order in orders:
          #      all_text += '<li>' + order.product_id + ',' + order.quantity + '</li>'
          # all_text += '</ul>'
          return users[0]
     
     except Exception as e:
          # e holds description of the error
          error_text = "<p>The error:<br>" + str(e) + "</p>"
          hed = '<h1>Something is broken.</h1>'
          return hed + error_text
    
# homepage route
@app.route('/')
def home():
     return render_template('homepage.html')

# loginpage route
@app.route('/login', methods=['GET', 'POST'])
def login():
     form = LoginForm()
     if form.validate_on_submit():
          user = User.query.filter_by(username=form.username.data).first()
          if user:
               if check_password_hash(user.password, form.password.data):
                    login_user(user)
                    session['username'] = user.username
                    return redirect(url_for('dashboard'))
          else:
               flash('Invalid username or password', 'error')
     return render_template('login.html', form=form)

# dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
     return render_template('dashboard.html')

# view products
@app.route('/view_product', methods=['GET', 'POST'])
@login_required
def view_product():
     products = Product.query.all()
     return render_template('view-product.html', products=products)

# # view orders
# @app.route('/view_order', methods=['GET', 'POST'])
# @login_required
# def view_order():
#      orders = Order.query.all()
#      return render_template('view-order.html', orders=orders)

# view users
@app.route('/view_user', methods=['GET', 'POST'])
@login_required
def view_user():
     users = User.query.all()
     return render_template('view-user.html', users=users)

# add products
@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
     form = ProductAddForm()
     products = Product.query.all()
     if request.method == 'POST':
          if not form.validate_on_submit():
               flash('All fields are required.')
               return render_template('add-product.html', form=form)
          
          # Create new Product entry
          prod = Product(
                    name = form.name.data,
                    price = form.price.data,
                    category = form.category.data,
                    description= form.description.data)
          
     if request.method == 'GET':
          return render_template('add-product.html', form=form)
     
# add orders
# @app.route('/add_order', methods=['GET', 'POST'])
# @login_required
# def add_order():
#      form = OrderAddForm()
#      orders = Order.query.all()
#      if request.method == 'POST':
#           if not form.validate_on_submit():
#                flash('All fields are required.')
#                return render_template('add-order.html', form=form)
          
#           # Create new Order
#           ins = User(
#                     first_name = form.first_name.data,
#                     last_name = form.last_name.data,
#                     username = form.username.data,
#                     password = hpw)
          
#      if request.method == 'GET':
#           return render_template('add-order.html', form=form)
     
# add users
@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
     form = UserAddForm()
     if not form.validate_on_submit():
          flash('All fields are required.')
          return render_template('add-user.html', form=form)
     else:
          f_name = form.first_name.data
          l_name = form.last_name.data
          un = form.username.data
          pw = form.password.data
          rl = form.role.data

          # Check if the username is already taken
          existing_user = User.query.filter_by(username=form.username.data).first()
          if existing_user:
               flash('Username is already taken.')
               return redirect(url_for('add_user'))
          
          # Check password validity before hashing
          if not pw:
               flash('Password is required.')
               return render_template('add-user.html', form=form)

          hpw = bcrypt.generate_password_hash(pw).decode('utf-8')

          # Create new User
          ins = User(
                    first_name = f_name,
                    last_name = l_name,
                    username = un,
                    password = hpw,
                    role = rl)
          
          db.session.add(ins)
          db.session.commit()
          flash('Submited')
          return redirect(url_for("view_user"))
          # if  bcrypt.check_password_hash(hpw, ins.password):
          #      db.session.add(ins)
          #      db.session.commit()
          #      flash('Submited')
          #      return redirect(url_for("view_user"))
          

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
     logout_user()
     return redirect(url_for('login'))

# Delete from database
@app.route('/add_user/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
     user = User.query.get_or_404(user_id)
     db.session.delete(user)
     db.session.commit()
     return render_template('view-user.html')

# @app.route('/add_product/<int:product_id>', methods=['GET', 'POST'])
# def delete_product(product_id):
#      product = Product.query.get_or_404(product_id)
#      db.session.delete(product)
#      db.session.commit()
#      return render_template('view-product.html')

# @app.route('/add_order/<int:order_id>', methods=['GET', 'POST'])
# def delete_order(order_id):
#      order = Order.query.get_or_404(order_id)
#      db.session.delete(order)
#      db.session.commit()
#      return render_template('view-order.html')

