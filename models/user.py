import hashlib

from passlib.handlers.bcrypt import bcrypt_sha256

from . import db

users_company = db.Table('users_company',
    db.Column('users_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    db.Column('company_id', db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'), primary_key=True)
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    account_permission = db.Column(db.Integer, nullable=False)

    def __init__(self, username, password, role_id, account_permission):
        self.username = username
        self.password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        self.role_id = role_id
        self.account_permission = account_permission


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    role_permission = db.Column(db.Integer, nullable=False)
    def __init__(self, id, role, permission):
        self.id = id
        self.role = role
        self.permission = permission

class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship('User', secondary=users_company, lazy='subquery',
        backref=db.backref('companies', lazy=True))
    def __init__(self, id):
        self.id = id



class Permissions:
    USER = 0x1
    ADMIN = 0x7
    COMPANY_LISTS = 0x2
    COMPANY_INFO = 0x8
