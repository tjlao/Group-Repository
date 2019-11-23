import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
products_db = myclient["products"]
order_management_db = myclient["order_management"]

def create_order(order):
    orders_coll = order_management_db['orders']
    orders_coll.insert(order)

def get_product(code):
    products_coll = products_db["products"]
    product = products_coll.find_one({"code":code})
    return product

def get_products():
    product_list = []
    products_coll = products_db["products"]

    for p in products_coll.find({}):
        product_list.append(p)
    return product_list

def get_orders(user_now):
    order_list = []
    order_details = []
    orders_coll = order_management_db['orders']

    for o in orders_coll.find({"username": user_now}):
        order_list.append(o)
    return order_list

def get_branch(code):
    branches_coll = products_db["branches"]
    branch = branches_coll.find_one({"code":code})
    return branch

def get_branches():
    branch_list = []
    branches_coll = products_db["branches"]

    for j in branches_coll.find({}):
        branch_list.append(j)
    return branch_list

def get_user(username):
    customers_coll = order_management_db['customers']
    user = customers_coll.find_one({"username":username})
    return user

def get_usernow(order):
    orders_coll = order_management_db['orders']
    return orders_coll

def check_user_order(user_now):
    orders_coll = order_management_db['orders']
    num_user_orders = []
    num_user_orders = orders_coll.count({"username":user_now})
    return num_user_orders

def change_db(user_user, new1):
    pw_coll = order_management_db['customers']
    customer = {"username":user_user}
    change = {"$set": {"password":new1}}

    pw_coll.find_one_and_update(customer,change)

    return
