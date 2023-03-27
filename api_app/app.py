from flask import Flask, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#create entension
db = SQLAlchemy()
ma = Marshmallow()
#init app
app=Flask(__name__)

#with app.app_context():

basedir = os.path.abspath(os.path.dirname(__file__))

#setting up databse
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init app with database extension
db.init_app(app)

# db = SQLAlchemy(app)
#init Marshmallow
# ma = Marshmallow(app)
#Creat Product Class/Model and our fields of interest
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

with app.app_context():
    db.create_all()

# Define output format with marshmallow, i.e Fields to expose Product)
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')

# Init product schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

#create a product
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']


    new_product = Product(name, description, price, qty)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


# Return all products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    #all_products = Product.Query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# To return or Get a single product
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)


# Update a product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    product.name = name
    product.description = description
    product.price = price
    product.qty = qty

    db.session.commit()

    return product_schema.jsonify(product)

# To delete a single product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)    
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)

#run server
if __name__ == '__main__':
    app.run(debug=True)