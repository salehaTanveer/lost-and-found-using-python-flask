from datetime import timedelta
from flask import jsonify, render_template, session, redirect, url_for, Blueprint, request
from functools import wraps
from dbmodels import *
from werkzeug.exceptions import abort
from validators import *

app.secret_key = "secretkey"


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:  # check if session exists
            return f(*args, **kwargs)
        else:
            return jsonify("Login required. No active session")

    return wrap


# redirect default route to login
@app.route('/')
def redirect_url():
    return redirect(url_for('login'))


# register route
@app.route('/register/', methods=['POST'])
def registration():
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        abort(400)  # missing arguments
    if password_is_valid(password) is None:
        abort(400)
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user

    new_user = User(username, password)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


# login route
@app.route('/login', methods=['GET'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        existing_user = User.query.filter_by(username=username).first()

        if existing_user is not None:
            if existing_user.password == password:
                session['user_id'] = existing_user.id
                session['logged_in'] = True
                app.permanent_session_lifetime = timedelta(minutes=5)
                return user_schema.jsonify(existing_user)
            else:
                abort(403)  # wrong password
        else:
            abort(400)  # existing user
    except:
        return jsonify("connection error")


# logout
@app.route('/logout', methods=['DELETE'])
@login_required
def logout():
    try:
        session.pop('logged_in', None)  # end session
        session.pop('user_id', None)  # clear user_id
        return jsonify("logged out. Session closed")
    except:
        return jsonify("error")


@app.route('/home')
@login_required
def home():
    return render_template('Home.html')  # render home page


# get all products
@app.route("/search", methods=['GET'])
@login_required
def get_all_products():
    try:
        all_products = Product.query.all()
        result = products_schema.dump(all_products)
        return jsonify(result)
    except:
        return jsonify("error")


# Get Single Product
@app.route('/search/<id>', methods=['GET'])
@login_required
def get_product(id):
    try:
        product = Product.query.get(id)
        return product_schema.jsonify(product)
    except:
        return jsonify("error")


'''# Get Product by name
@app.route('/search/string:<name>', methods=['GET'])
@login_required
def get_product_by_name(name):
    try:
        product = Product.query.filter_by(name=name).all()
        return product_schema.jsonify(product)
    except:
        return jsonify("error")'''


# Update a Product
@app.route('/search/<int:id>/update', methods=['PUT'])
@login_required
def update_product(id):
    try:
        product = Product.query.get(id)
        if product is None:
            return jsonify("Product id does not exist")

        name = request.json['name']
        description = request.json['description']
        location = request.json['location']
        Date = request.json['Date']
        Status = request.json['Status']

        # pass new data
        product.name = name
        product.description = description
        product.location = location
        product.Date = Date
        product.Status = Status

        db.session.commit()

        return product_schema.jsonify(product)
    except:
        return jsonify("error")


# Delete a Product
@app.route('/search/delete/<int:id>', methods=['DELETE'])
@login_required
def delete_product(id):
    try:
        product = Product.query.get(id)
        db.session.delete(product)
        db.session.commit()
        return product_schema.jsonify(product)
    except:
        return jsonify("error")


# insert a new product
@app.route('/insert', methods=['POST'])
@login_required
def add_product():
    try:
        name = request.json['name']
        description = request.json['description']
        location = request.json['location']
        Date = request.json['Date']
        Status = request.json['Status']
        user_id = session['user_id']

        if name is None or description is None or location is None or Date is None or Status is None:
            abort(400)

        new_product = Product(name, description, location, Date, Status, user_id)

        db.session.add(new_product)
        db.session.commit()

        return product_schema.jsonify(new_product)
    except:
        return jsonify("error")


# pagination
'''@app.route('/products', methods=['GET'])
@app.route('/products/page/<int:page>')
def all_products(page=1):
    USERS_PER_PAGE = 2
    try:
        product_list = Product.query.order_by(
            Product.id.desc()
        ).paginate(page, per_page=USERS_PER_PAGE)
    except OperationalError:
        product_list = None
        return products_schema.jsonify(product_list)'''

'''
# Run Server
if __name__ == '__main__':
    app.run(debug=True)
'''
