from flask import Flask, request, render_template, session, redirect, Response, send_file, flash

from sqlalchemy import and_, __version__

import database
from models import Product
import os
import json
import base64
import uuid
import boto3

application = app = Flask(__name__)
app.secret_key = os.urandom(64)
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



@app.route('/products', methods=['GET', 'POST', 'DELETE', 'PUT'])
def dealership_react():
    error = None
    if request.method == 'GET':
        return get_products()

    if request.method == 'POST':
        for instance in db_instance.query(User).filter(
                and_(User.user_email == session.get('email'), User.user_type == 'Dealer')):
            exp = Dealership(
                dealership_name='dealership_name',
                dealership_email='dealership_email',
                dealership_url='dealership_url',
                dealership_phone='dealership_phone',
                dealership_picture='dealership_img',
                dealership_district='dealership_district')

            dealership = Dealership(
                dealership_name=request.form['dealership_name'],
                dealership_email=request.form['dealership_email'],
                dealership_url=request.form['dealership_url'],
                dealership_phone=request.form['dealership_phone'],
                dealership_picture=img_URL,
                dealership_district=request.form['dealership_district'])

            instance.user_dealerships.append(dealership)

        db_instance.commit()

        return get_products()

    if request.method == 'DELETE':
        dealership_id = request.form['dealership_id']

        for instance in db_instance.query(User).filter(User.user_email == session.get('email')):
            dealership = db_instance.query(Dealership).filter(and_(Dealership.dealership_id == dealership_id),
                                                              (instance.user_id == Dealership.user_id)).first()

            deleteImageBoto3(dealership.car_picture)

            db_instance.query(Dealership).filter(and_(Dealership.dealership_id == dealership_id),
                                                 (instance.user_id == Dealership.user_id)).delete()

            db_instance.commit()

        return get_dealerships()

    if request.method == 'PUT':
        print("1")
        for instance in db_instance.query(User).filter(User.user_email == session.get('email')):
            print("2")
            img = request.form['data_uri']

            picture = request.form['dealership_picture']

            if img == picture:
                print("NOT")
                dealership = Dealership(
                    dealership_picture=request.form['dealership_picture'],
                    dealership_name=request.form['dealership_name'],
                    dealership_email=request.form['dealership_email'],
                    dealership_url=request.form['dealership_url'],
                    dealership_phone=request.form['dealership_phone'],
                    dealership_district=request.form['dealership_district'])
                dealership_id = request.form['dealership_id']
                db_instance.query(Dealership).filter(
                    and_(Dealership.dealership_id == dealership_id, instance.user_id == Dealership.user_id)).update(
                    {
                        "dealership_name": dealership.dealership_name,
                        "dealership_picture": dealership.dealership_picture,
                        "dealership_email": dealership.dealership_email,
                        "dealership_url": dealership.dealership_url,
                        "dealership_phone": dealership.dealership_phone,
                        "dealership_district": dealership.dealership_district})

            else:
                print("NEW")
                img_URL = decodeImageBoto3(img)
                dealership = Dealership(
                    dealership_picture=img_URL,
                    dealership_name=request.form['dealership_name'],
                    dealership_email=request.form['dealership_email'],
                    dealership_url=request.form['dealership_url'],
                    dealership_phone=request.form['dealership_phone'],
                    dealership_district=request.form['dealership_district'])
                dealership_id = request.form['dealership_id']
                db_instance.query(Dealership).filter(
                    and_(Dealership.dealership_id == dealership_id, instance.user_id == Dealership.user_id)).update(
                    {
                        "dealership_name": dealership.dealership_name,
                        "dealership_picture": dealership.dealership_picture,
                        "dealership_email": dealership.dealership_email,
                        "dealership_url": dealership.dealership_url,
                        "dealership_phone": dealership.dealership_phone,
                        "dealership_district": dealership.dealership_district})
        print("2")
        db_instance.commit()
        print("3")
        return get_products()








if __name__ == "__main__":
    application.debug = True
    application.run(host="0.0.0.0")

