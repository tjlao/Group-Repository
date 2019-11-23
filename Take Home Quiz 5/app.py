from flask import Flask, redirect
from flask import render_template
from flask import request
from flask import session
import database as db
import authentication
import logging
import ordermanagement as om

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
    loginerror = "Incorrect username or password."
    return render_template('/login.html', loginerror = loginerror)

@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("cart", None)
    return redirect ('/')


@app.route('/change', methods = ['POST'])
def change():
    oldpw = request.form.get("old")
    new1 = request.form.get("new1")
    new2 = request.form.get("new2")
    usernow1 = session["user"]
    user_user = usernow1["username"]
    user_pw = usernow1["password"]

    if oldpw != user_pw:
        change_error = "Incorrect Password"
        return render_template('/change_pw.html', change_error=change_error)
    elif new1 != new2:
        change_error = "Passwords do not match"
        return render_template('/change_pw.html', change_error=change_error)
    else:
        change_now = db.change_db(user_user, new1)
        change_error = "Update Password Success"
        return render_template('/change_pw.html', change_error=change_error)

@app.route('/change_pw')
def change_pw():
    return render_template('change_pw.html')

@app.route('/addtocart' , methods = ['GET', 'POST'])
def addtocart():
    qty = request.form.get('Quantity', '')
    code = request.form.get('code', '')
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
    qty_all = request.form.getlist('qty_cart')
    price = request.form.getlist('price')
    code = request.form.getlist('code')
    name = request.form.getlist('name')

    for i in range(0,len(qty_all)):
        item=dict()
        item["qty"] = int(qty_all[i])
        item["price"] = int(price[i])
        item["name"] = name[i]
        item["code"] = int(code[i])
        item["subtotal"] = item["price"]*item["qty"]

        if(session.get("cart") is None):
            session["cart"]={}

        cart = session["cart"]
        cart[code[i]] = item
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

@app.route('/checkout')
def checkout():
    # clear cart in session memory upon checkout
    om.create_order_from_cart()
    session.pop("cart",None)
    return redirect('/ordercomplete')

@app.route('/ordercomplete')
def ordercomplete():
    return render_template('ordercomplete.html')

@app.route('/orders')
def orders():
    user_ = session["user"]
    user_now = user_["username"]
    order_yes = om.check_user(user_now)

    if order_yes == True:
        order_list = db.get_orders(user_now)
        noorder = False

        return render_template('orders.html', order_list=order_list, noorder=noorder)
    else:
        noorder = True
        return render_template('orders.html', noorder=noorder)

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
