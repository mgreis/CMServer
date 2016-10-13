#author = mgreis@student.dei.uc.pt
from flask import Flask, request, Response

from sqlalchemy import __version__, and_
import database
from models import Product, User


application = app = Flask(__name__)


#app.secret_key = os.urandom(64)
db_instance = database.init_db()

print("SQLAlchemy version: " + __version__)










def get_products(user_id):
    all_products = []
    for instance in db_instance.query(Product).filter(Product.user_id == user_id):
        all_products.append(instance.__repr__())

    string = "[ " + " , ".join(all_products) + " ]"
    print(string)

    return Response(string, mimetype='application/json',
                    headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})

def get_product(user_id, product_id):
    product = []
    for instance in db_instance.query(Product).filter(and_(Product.user_id == user_id)(Product.product_id == product_id)):
        product.append(instance.__repr__())
    string = "[ " + " , ".join(product) + " ]"
    print(string)

    return Response(string, mimetype='application/json',
                    headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})


def get_user(user_email,user_password):
    user = []
    for instance in db_instance.query(User).filter(and_(User.user_email == user_email), (User.user_password == user_password)):
        user.append(instance.__repr__())
    string = "[ " + " , ".join(user) + " ]"
    print(string)

    return Response(string, mimetype='application/json',
                    headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})


@app.route('/users', methods=['GET','POST'])
def users():
    if request.method == 'GET':
        user_email = request.form['user_email']
        user_password = request.form['user_password']
        return get_user(user_email, user_password)
    if request.method == 'POST':
        user = User(
            user_email = request.form['user_email'],
            user_password = request.form['user_password'])
        db_instance.query(User).append(user)
        db_instance.commit()
        return get_user(request.form['user_email'],request.form['user_password'])


@app.route('/products/<path:user_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def products(user_id):
    error = None
    if request.method == 'GET':
        return get_products(user_id)

    if request.method == 'POST':
        product = Product(
            product_name=request.form['product_name'],
            product_price=request.form['product_price'],
            product_qty=request.form['product_qty'],
            user_id=request.form['user_id'])

        db_instance.query(Product).append(product)

        db_instance.commit()

        return get_products(user_id)

    if request.method == 'DELETE':
       ''' product_id = request.form['product_id']
        db_instance.query(Product).filter(Product.product_id == product_id)
        db_instance.commit()'''
       return get_products()

    if request.method == 'PUT':
        '''product_id = request.form['product_id']
        db_instance.query(Product).filter(
            Product.product_id == product_id).update(
            {
                "product_name" : request.form['product_name'],
                "product_price" : request.form['product_price'],
                "product_qty" : request.form['product_qty']})
        db_instance.commit()'''
        return get_products()


@app.route('/products/<path:user_id>/<path:product_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def product(user_id,product_id):
    error = None
    if request.method == 'GET':

        return get_product(user_id,product_id)

    if request.method == 'POST':
        '''product = Product(
            product_name=request.form['product_name'],
            product_price=request.form['product_price'],
            product_qty=request.form['product_qty'])

        db_instance.query(Product).user_dealerships.append(product)

        db_instance.commit()'''

        return get_product(user_id,product_id)

    if request.method == 'DELETE':
        db_instance.query(Product).filter(and_(Product.user_id == user_id), (Product.product_id == product_id)).delete()
        db_instance.commit()

        return get_products()

    if request.method == 'PUT':
        db_instance.query(Product).filter(and_(Product.product_id == product_id), (Product.user_id == user_id)).update(
        {
            "product_name" : request.form['product_name'],
            "product_price" : request.form['product_price'],
            "product_qty" : request.form['product_qty']})
        db_instance.commit()
        return get_product(user_id, product_id)





if __name__ == "__main__":
    application.debug = True
    application.run(host="0.0.0.0")

