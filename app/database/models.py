from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    clients = db.relationship('Client', backref='user', lazy='dynamic')
    employees = db.relationship('Employee', backref='user', lazy='dynamic')
    trips = db.relationship('Trip', backref='user', lazy='dynamic')
    trucks = db.relationship('Truck', backref='user', lazy='dynamic')
    maintenance = db.relationship('Maintenance', backref='user', lazy='dynamic')
    stops = db.relationship('Stops', backref='user', lazy='dynamic')
    invoices = db.relationship('Invoice', backref='user', lazy='dynamic' )
    diesel = db.relationship('Diesel', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    company_name = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    fax = db.Column(db.String(120))
    address = db.Column(db.String(120))
    zipcode = db.Column(db.Integer())
    city = db.Column(db.String(64))
    state = db.Column(db.String(2))

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name =  db.Column(db.String(64), index=True)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    fax = db.Column(db.String(120))
    address = db.Column(db.String(140))
    zipcode = db.Column(db.String(10))
    city = db.Column(db.String(64))
    state = db.Column(db.String(2))
    country = db.Column(db.String(64))
    mc_number = db.Column(db.String(20))
    dot_number = db.Column(db.String(20))
    quickpay = db.Column(db.String(1))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    quickpay_info = db.relationship('Quickpay', backref='client', lazy="dynamic")
    trip_hist = db.relationship('Trip', backref='client', lazy='dynamic')
    inv_hist = db.relationship('Invoice', backref='client', lazy='dynamic')

class Quickpay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    pay_percentage = db.Column(db.String(5))
    send_to = db.Column(db.String(120))
    send_to_type = db.Column(db.String(20))

class Truck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    VIN_number = db.Column(db.String(64))
    reg_number = db.Column(db.String(64))
    model = db.Column(db.String(64))
    maintenance_hist = db.relationship('Maintenance', backref='truck', lazy="dynamic")
    diesel_hist = db.relationship('Diesel', backref='truck', lazy='dynamic')

class  Maintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    truck_id = db.Column(db.Integer, db.ForeignKey('truck.id'))
    price = db.Column(db.Float())
    desc = db.Column(db.Float())

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    em_firstname = db.Column(db.String(64))
    em_lastname = db.Column(db.String(64))
    trip_hist = db.relationship('Trip', backref='truck', lazy='dynamic')

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    truck_id = db.Column(db.Integer, db.ForeignKey('truck.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    trip_diesel_hist = db.relationship('Diesel', backref='trip', lazy='dynamic')
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    stops_hist = db.relationship('Stops', backref='trip', lazy='dynamic')

class Diesel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    truck_id = db.Column(db.Integer, db.ForeignKey('truck.id'))
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
    price = db.Column(db.Float())
    desc = db.Column(db.String(120))
    gal = db.Column(db.Float())

class Stops(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
    origin_route = db.Column(db.String(64))
    origin_state = db.Column(db.String(2))
    dest_route = db.Column(db.String(64))
    dest_state = db.Column(db.String(2))
    mileage = db.Column(db.Float())

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    price_total = db.Column(db.Float())
    paid_toggle = db.Column(db.String(4))