from flask import Flask, redirect
from flask import render_template
from flask import request
from flask import session
import database as db
import authentication
import logging

app = Flask(__name__)

# Set the secret key to some random bytes.
# Keep this really secret!
app.secret_key = b's@g@d@c0ff33'

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)

@app.route( '/login' , methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route( '/auth' , methods = ['POST'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')

    is_successful, user = authentication.login(username, password)

    app.logger.info('%s', is_successful)

    if(is_successful):
        session["user"] = user
        return redirect ('/')
    else:
        return redirect ('/login_error')

@app.route('/login_error')
def login_error():
    return render_template('/login_error.html')

@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("cart", None)
    return redirect ('/')

@app.route('/addtocart' , methods = ['GET', 'POST'])
def addtocart():
    qty = request.form.get('Quantity', '')
    code = request.args.get('code', '')
    product = db.get_product(int(code))
    item=dict()
    # A click to add a product translates to a
    # quantity of 1 for now
    item["qty"] = int(qty)
    item["code"] = code
    item["name"] = product["name"]
    item["price"] = product["price"]
    item["subtotal"] = product["price"]*item["qty"]

    if(session.get("cart") is None):
        session["cart"]={}

    cart = session["cart"]
    cart[code] = item
    session["cart"] = cart
    return redirect('/cart')

@app.route('/updatecart' , methods = ['POST'])
def updatecart():
    qty_all = request.form.get('qty_cart', '')
    price = request.form.get('price', '')
    code = request.form.get('code', '')
    name = request.form.get('name', '')
    item=dict()

    for i in qty_all:
        item["qty"] = int(qty_all)
        item["price"] = int(price)
        item["name"] = name
        item["subtotal"] = item["price"]*item["qty"]

        if(session.get("cart") is None):
            session["cart"]={}

        cart = session["cart"]
        cart[code] = item
        session["cart"] = cart
        return redirect('/cart')

@app.route('/clearcart')
def clearcart():
    del session["cart"]
    return redirect('/cart')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/')
def index():
    return render_template('index.html', page="Index")

@app.route('/products')
def products():
    product_list = db.get_products()
    return render_template('products.html', page="Products", product_list=product_list)

@app.route('/productdetails')
def productdetails():
    code = request.args.get('code', '')
    product = db.get_product(int(code))

    return render_template('productdetails.html', code=code, product=product)

@app.route('/branches')
def branches():
    branch_list = db.get_branches()
    return render_template('branches.html', page="Branches", branch_list=branch_list)

@app.route('/branchdetails')
def branchdetials():
    code = request.args.get('code', '')
    branch = db.get_branch(int(code))

    return render_template('branchdetails.html', code=code, branch=branch)

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', page="About Us")
