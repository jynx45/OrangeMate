from datetime import datetime
from app import app as flask_app
from app import db
from sqlalchemy.inspection import inspect

flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'


class ModelMixin:
    """Provide dict-like interface to db.Model subclasses."""

    def __getitem__(self, key):
        """Expose object attributes like dict values."""
        return getattr(self, key)

    def keys(self):
        """Identify what db columns we have."""
        return inspect(self).attrs.keys()


class TimestampMixin(object):
    created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


class User(TimestampMixin, db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


class Fund(TimestampMixin, db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False,
    )
    user = db.relationship(
        'User',
    )
    amount = db.Column(db.Integer, nullable=False)
    source_instrument = db.Column(db.String(120), nullable=False)
    transaction_type = db.Column(db.String(120), nullable=False)


class TransactionToken(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token_id = db.Column(db.String(80), unique=True, nullable=False)
    used = db.Column(db.Boolean)


from flask.json import JSONEncoder

class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        # Optional: convert datetime objects to ISO format
        try:
            return obj.isoformat()
        except Exception:
            return dict(obj)

flask_app.json_encoder = MyJSONEncoder

db.create_all()
