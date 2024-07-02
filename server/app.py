#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(  bakeries,   200  )

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()
    bakery_serialized = bakery.to_dict()
    return make_response ( bakery_serialized, 200  )

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )

@app.route('/baked_goods', methods = ['GET', 'POST'])
def post_baked_goods():
    # If a GET request
    # Send a GET request to the Database to retrieve information about all the baked goods.
    if request.method == 'GET':
        # Create a list to store all the baked goods dictionaries.
        baked_goods_list = list()
        # Query the database for all the baked goods present. Assign to the variable baked_goods.
        baked_goods = BakedGood.query.all()
        # Loop through the baked goods retrieved from the database.
        # Allows us to create a dict for each of the baked goods objects in the database.
        for baked_good in baked_goods:
            # Create a dict for each baked_good object.
            baked_good_dict = baked_good.to_dict()
            # Append each 'baked_good_dict' to the 'baked_goods_list' list.
            baked_goods_list.append(baked_good_dict)

            response = make_response(
                baked_goods_list, 200  # 200 status code for HTTP OK.
            )

            return response
        
        # if the request is a POST request
    elif request.method == "POST":
        # Create a new baked_good object in a form
        new_baked_good = BakedGood(
            name=request.form.get("name"),
            price=request.form.get("price"),
            created_at=request.form.get("created_at"),
            bakery_id=request.form.get("bakery_id"),
        )
        # Add the new baked_good object to the database.
        db.session.add(new_baked_good)
        # Commit the changes to the database.
        db.session.commit()
        # Create a dict of the object.
        baked_good_dict = new_baked_good.to_dict()
        # Create a response object.
        response = make_response(
            baked_good_dict, 201  # 201 status code for HTTP Created.
        )

        return response
    
# Route to implement PATCH(Update) to Update the bakery name.
@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def update_bakery_name(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if bakery == None:
        response_body = {
            "message": "Bakery not found in Database."
        }
        response = make_response(response_body, 404) # Not found status code.

        return response
    
    else:
        if request.method == 'GET':
            bakery_dict = bakery.to_dict()

            response = make_response(bakery_dict, 200)

            return response
        
        elif request.method == 'PATCH':
            for attr in request.form:
                setattr(bakery, attr, request.form.get(attr))

            db.session.add(bakery)
            db.session.commit()

            bakery_dict = bakery.to_dict()

            response = make_response(bakery_dict, 200)

            return response

@app.route('/baked_goods/<int:id>', methods = ['GET', 'DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.filter_by(id=id).first()
    if baked_good == None:
        response_body = {
            "message": "Baked Good not found in Database"
        }
        response = make_response(response_body, 404) # Not found status code.

        return response
    
    else:
        if request.method == 'GET':
            baked_good_dict = baked_good.to_dict()

            response = make_response(baked_good_dict, 200)

            return response
        
        elif request.method == 'DELETE':
            db.session.delete(baked_good)
            db.session.commit()

            response_body = {
                "message": "Baked Good deleted successfully."
            }
            response = make_response(response_body, 200)

            return response



    pass
if __name__ == '__main__':
    app.run(port=5555, debug=True)