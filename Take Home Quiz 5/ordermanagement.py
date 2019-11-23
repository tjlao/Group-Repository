import database as db
from flask import session
from datetime import datetime


def create_order_from_cart():
    order = {}
    order.setdefault("username",session["user"]["username"])
    order.setdefault("orderdate",datetime.utcnow())
    order_details = []
    cart = session["cart"]
    for key, value in cart.items():
        order_details.append({"code":key,"name":value["name"],"qty":value["qty"],"subtotal":value["subtotal"]})
    order.setdefault("details",order_details)
    db.create_order(order)

def check_user(user_now):
    number_orders = 0
    number_orders = db.check_user_order(user_now)

    if number_orders > 0:
        return True
    else:
        return False
