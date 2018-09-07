from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    clients = db.relationship('Client', backref='user', lazy='dynamic')

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

class Quickpay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    pay_percentage = db.Column(db.String(5))
    send_to = db.Column(db.String(120))
    send_to_type = db.Column(db.String(20))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))