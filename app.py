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

# ______ Initialize Table(s) ______ 
# Create a table for each of the following:
# 1. Users
# 2. Products
# 3. Orders
# 4. Order Product Association

class Base(DeclarativeBase):
    pass

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

# ______ Initialize Route(s) ______
# Create a route for each of the following:
# User Endpoints
# 1. GET/users
# 2. GET/users/<user_id>
# 3. POST/users
# 4. PUT/users/<user_id>
# 5. DELETE/users/<user_id>


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


