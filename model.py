from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import app as flask_app

flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(flask_app)




class TimestampMixin(object):
    created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


class User(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


class Fund(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False,
    )
    user = db.relationship(
        'User',
        backref=db.backref('users', lazy=True),
    )
    amount = db.Column(db.Integer, nullable=False)
    source_instrument = db.Column(db.String(120), nullable=False)
    transaction_type = db.Column(db.String(120), nullable=False)


class TransactionToken(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token_id = db.Column(db.String(80), unique=True, nullable=False)
    used = db.Column(db.Boolean)

db.create_all()
