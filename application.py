# author = mgreis@student.dei.uc.pt
from flask import Flask, request, Response, abort

from sqlalchemy import __version__, and_, exc

import database
from models import Product, User

application = app = Flask(__name__)

db_instance = database.init_db()

print("SQLAlchemy version: " + __version__)




def get_products(user_id):
    all_products = []
    exists = False
    for instance in db_instance.query(Product).filter(Product.user_id == user_id):
        exists = True
        all_products.append(instance.__repr__())
    if exists:
        string = "[ " + " , ".join(all_products) + " ]"
        return Response(string, mimetype='application/json',
                        headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})
    else:
        return abort(404)


def get_user(user_email, user_password):
    user = []
    exists = False
    for instance in db_instance.query(User).filter(and_(User.user_email == user_email),
                                                   (User.user_password == user_password)):
        user.append(instance.__repr__())
        exists = True
    if exists:
        string = "[ " + " , ".join(user) + " ]"
        return Response(string, mimetype='application/json',
                        headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})
    else:
        return abort(403)


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        user_email = request.args.get('user_email')
        user_password = request.args.get('user_password')
        return get_user(user_email, user_password)
    if request.method == 'POST':
        # print (request.form['user_email'])
        # print (request.form['user_password'])
        try:
            user = User(
                user_email=request.form['user_email'],
                user_password=request.form['user_password'])
            db_instance.add(user)
            db_instance.commit()
        except exc.SQLAlchemyError:
            return abort(403)

        else:
            return get_user(request.form['user_email'], request.form['user_password'])


@app.route('/products/<path:user_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def products(user_id):
    if request.method == 'GET':
        return get_products(user_id)

    if request.method == 'POST':
        try:
            new_product = Product(
                product_name=request.form['product_name'],
                product_price=request.form['product_price'],
                product_qty=request.form['product_qty'],
                user_id=user_id)

            db_instance.add(new_product)
            db_instance.commit()
        except exc.SQLAlchemyError:
            return(abort(403))

        else:
            return '', 200

    if request.method == 'DELETE':
        return abort(403)

    if request.method == 'PUT':
        return abort(403)


@app.route('/products/<path:user_id>/<path:product_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def product(user_id, product_id):

    if request.method == 'GET':
        return abort(403)

    if request.method == 'POST':
        return abort(403)

    if request.method == 'DELETE':
        db_instance.query(Product).filter(and_(Product.user_id == user_id), (Product.product_id == product_id)).delete()
        db_instance.commit()

        return '', 200

    if request.method == 'PUT':
        db_instance.query(Product).filter(and_(Product.product_id == product_id), (Product.user_id == user_id)).update(
            {
                "product_name": request.form['product_name'],
                "product_price": request.form['product_price'],
                "product_qty": request.form['product_qty']})
        db_instance.commit()
        return '', 200


if __name__ == "__main__":
    application.debug = True
    application.run(host="0.0.0.0", port=80)
