# Import Packages
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import  DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, Table, Column, String, Integer
from marshmallow import ValidationError
from typing import List, Optional
import os

# ______ Initialize Flask App ______ 
app = Flask(__name__)


# ______ Initialize Database ______
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Saiouma2018@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Base(DeclarativeBase):
    pass

#_________ Initialize SQLAclchemy & Marshmallow __________
db = SQLAlchemy(model_class= Base)
db.init_app(app)
ma = Marshmallow(app)

# ______ Initialize Table(s) ______ 
# Create a table for each of the following:
# 1. Users
# 2. Products
# 3. Orders
# 4. Order Product Association

# Models

class User(Base):
    __tablename__ = 'users' # Create a table namd 'users'
    # Define the columns in the table
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    orders: Mapped[List['Order']] = relationship('Order', back_populates='user')

class Product(Base):
    __tablename__ = 'products'# Create a table named 'products'
    # Define the columns in the table
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    price: Mapped[float] = mapped_column(Integer, nullable=False)
    orders: Mapped[List['Order']] = relationship('Order', secondary='order_product', back_populates='products')

class Order(Base):
    __tablename__ = 'orders' #Create a table named 'orders'
    # Define the columns in the table
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped[User] = relationship('User', back_populates='orders')
    products: Mapped[List[Product]] = relationship('Product', secondary='order_product', back_populates='orders')

# Create an association table for the many-to-many relationship between orders and products
# The table will have two foreign keys: order_id and product_id
order_product = Table('order_product', Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True)
)

# ______ Initialize Schema(s) ______ 
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order

class OrderProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = order_product

user_schema = UserSchema()
users_schema = UserSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

# ______ Initialize Route(s) ______
# Create a route for each of the following:
# User Endpoints
# 1. GET/users
# 2. GET/users/<user_id>
# 3. POST/users
# 4. PUT/users/<user_id>
# 5. DELETE/users/<user_id>

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return users_schema.jsonify(users)

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return user_schema.jsonify(user)
    else:
        return jsonify({"message": "User not found"}), 404
    
@app.route("/users", methods=["POST"])
def create_user():
    try:
        name = request.json["name"]
        email = request.json["email"]
        password = request.json["password"]
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)    
        db.session.commit()
        return user_schema.jsonify(new_user), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user= User.query.get(user_id)
    if user:
        try:
            name = request.json["name"]
            email = request.json["email"]
            password = request.json["password"]
            user.name = name
            user.email = email
            user.password = password
            db.session.commit()
            return user_schema.jsonify(user)
        except ValidationError as err:
            return jsonify(err.messages), 400
    else:
        return jsonify({"message": "User not found"}), 404

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user= User.query.get(user_id)
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            return user_schema.jsonify(user)
        except ValidationError as err:
            return jsonify(err.messages), 400
    else:
        return jsonify({"message": "User not found"}), 404



# Product Endpoints
# 1. GET/products
# 2. GET/products/<product_id>
# 3. POST/products
# 4. PUT/products/<product_id>
# 5. DELETE/products/<product_id>


# Order Endpoints
# 1. GET/orders/user/<user_id>: Get all orders for a user
# 2. GET/orders/<order_id>/products: Get all products in an order
# 3. POST/orders
# 4. PUT /orders/<order_id>/add_product/<product_id>: Add a product to an order (prevent duplicates)
# 5. DELETE/orders/<order_id>/remove_product: Remove a product from an order


