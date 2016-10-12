from flask import Flask, request, Response

from sqlalchemy import __version__

import database
from models import Product


application = app = Flask(__name__)


#app.secret_key = os.urandom(64)
db_instance = database.init_db()

print("SQLAlchemy version: " + __version__)




def get_products():
    all_products = []
    for instance in db_instance.query(Product):
        all_products.append(instance.__repr__())

    string = "[ " + " , ".join(all_products) + " ]"
    print(string)

    return Response(string, mimetype='application/json',
                    headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})

def get_product(product_id):
    product = []
    for instance in db_instance.query(Product).filter(Product.product_id==product_id):
        product.append(instance.__repr__())
    string = "[ " + " , ".join(product) + " ]"
    print(string)

    return Response(string, mimetype='application/json',
                    headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})


@app.route('/products', methods=['GET', 'POST', 'DELETE', 'PUT'])
def products():
    error = None
    if request.method == 'GET':
        return get_products()

    if request.method == 'POST':
        product = Product(
            product_name=request.form['product_name'],
            product_price=request.form['product_price'],
            product_qty=request.form['product_qty'])

        db_instance.query(Product).user_dealerships.append(product)

        db_instance.commit()

        return get_products()

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


@app.route('/products/<path:product_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def product(product_id):
    error = None
    if request.method == 'GET':

        return get_product(product_id)

    if request.method == 'POST':
        '''product = Product(
            product_name=request.form['product_name'],
            product_price=request.form['product_price'],
            product_qty=request.form['product_qty'])

        db_instance.query(Product).user_dealerships.append(product)

        db_instance.commit()'''

        return get_product(product_id)

    if request.method == 'DELETE':
        db_instance.query(Product).filter(Product.product_id == product_id).delete()
        db_instance.commit()

        return get_products()

    if request.method == 'PUT':
        db_instance.query(Product).filter(Product.product_id == product_id).update(
        {
            "product_name" : request.form['product_name'],
            "product_price" : request.form['product_price'],
            "product_qty" : request.form['product_qty']})
        db_instance.commit()
        return get_product(product_id)





if __name__ == "__main__":
    application.debug = True
    application.run(host="0.0.0.0")

