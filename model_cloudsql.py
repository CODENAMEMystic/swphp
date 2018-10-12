# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


builtin_list = list


db = SQLAlchemy()


def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)


def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data


# [START model]
class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    remain = db.Column(db.String(255))
    sold = db.Column(db.String(255))
    purchased = db.Column(db.String(255))
    dateOrdered = db.Column(db.String(255))


    def __repr__(self):
        return "<Inventory(name='%s', author=%s)" % (self.name, self.author)
 
class Person(db.Model):
    __tablename__ = 'person'

    person_name = db.Column(db.VARCHAR(50), primary_key=True)
    snapchat = db.Column(db.VARCHAR(50))
    address = db.Column(db.VARCHAR(50))
    moneyspent = db.Column(db.INT)
 


class Orders(db.Model):
 	__tablename__ = 'orders'
 	sold = db.Column(db.INT)
 	id = db.Column(db.INT, primary_key=True)
 	person_name = db.Column(db.VARCHAR(50))
 	item_name = db.Column(db.VARCHAR(50))
 	item_quantity = db.Column(db.INT)
 	requestDate = db.Column(db.VARCHAR(50))
 	
 	def __repr__(self):
 		return "<Orders(name='%s', author=%s)" % (self.person_name, self.item_name)
class Shipments(db.Model):
	__tablename__ = 'shipments'
	
	id = db.Column(db.INT, primary_key=True)
	orderDate = db.Column(db.VARCHAR(50))
	items = db.Column(db.VARCHAR(240))
	trackingCode = db.Column(db.VARCHAR(50))

    
# [END model]






# [START model]
class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    flavor = db.Column(db.String(255))
    publishedDate = db.Column(db.String(255))
    paymentamount = db.Column(db.String(255))

# [START model]
class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(50))
    password = db.Column(db.VARCHAR(50))
    authority = db.Column(db.INT)
    dateCreated = db.Column(db.VARCHAR(50))


    def __repr__(self):
        return "<Transaction(name='%s', author=%s)" % (self.name, self.author)
# [END model]


# [START list]
def list(limit=35, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Orders.query
             .order_by(Orders.id)
             .limit(limit)
             .offset(cursor))
    orders = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(orders) == limit else None
    return (orders, next_page)
    
def listI(limit=35, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Inventory.query
             .order_by(Inventory.id)
             .limit(limit)
             .offset(cursor))
    inventorys = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(inventorys) == limit else None
    return (inventorys, next_page)
    
# [START list]
def glist(limit=40, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Inventory.query
             .order_by(Inventory.name)
             .limit(limit)
             .offset(cursor))
    inventorys = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(inventorys) == limit else None
    return (inventorys, next_page)
# [END list]


def alist(limit=35, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Account.query
             .order_by(Account.name)
             .limit(limit)
             .offset(cursor))
    accounts = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(accounts) == limit else None
    return (accounts, next_page)
    
def slist(limit=35, cursor=None):
    cursor = int(cursor) if cursor else 0;
    query = (Shipments.query
             .order_by(Shipments.id)
             .limit(limit)
             .offset(cursor))
    shipment = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(shipment) == limit else None
    return (shipment, next_page)

# [END list]


# [START read]
def read(id):
	result = Orders.query.get(id)
	if not result:
		return None
	return from_sql(result)

def readI(id):
	result = Inventory.query.get(id)
	if not result:
		return None
	return from_sql(result)
    
    
def readAccount(name):
    result = Account.query.get(name)
    if not result:
        return None
    return from_sql(result)
# [END read]


# [START create]
def createAccount(data):
    account = Account(**data)
    
    db.session.add(account)
    db.session.commit()
    #orders = Orders.query.get(id)
    #for k, v in data.items():
    #	setattr(orders, k, v)
    #	db.session.commit()
    return from_sql(account)
# [END create]

def create(data):
    order = Orders(**data)
    
    db.session.add(order)
    db.session.commit()
    #orders = Orders.query.get(id)
    #for k, v in data.items():
    #	setattr(orders, k, v)
    #	db.session.commit()
    return from_sql(order)
    
def createI(data):
    inventory = Inventory(**data)
    
    db.session.add(inventory)
    db.session.commit()


# [START update]
def update(data, id):
    order = Orders.query.get(id)
    for k, v in data.items():
        setattr(order, k, v)
    db.session.commit()
    return from_sql(order)
    
    # [START update]
def updateAccount(data, id):
    account = Account.query.get(id)
    for k, v in data.items():
        setattr(order, k, v)
    db.session.commit()
    return from_sql(account)
# [END update]

# [START update]
def updateI(data, id):
	inventory = Inventory.query.get(id)
	for k, v in data.items():
		setattr(inventory, k, v)
		db.session.commit()
	return from_sql(inventory)
# [END update]


def delete(id):
    Orders.query.filter_by(id=id).delete()
    db.session.commit()


def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables createffd")


if __name__ == '__main__':
    _create_database()