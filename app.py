import json
import uuid
from flask import (
    Flask,
    jsonify,
    request,
)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
from model import (
    User,
    Fund,
    TransactionToken,
)


@app.route("/users", methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        user = User(**json.loads(request.data))
        db.session.add(user)
        db.session.commit()
        return jsonify(user)
    else:
        users = User.query.order_by(User.username).all()
        return jsonify(users)


@app.route("/users/<int:id>", methods=['GET'])
def user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user


@app.route("/users/<int:user_id>/funds", methods=['POST', 'GET'])
def user_fund(user_id):
    if request.method == 'POST':
        fund = Fund(user_id=user_id, **json.loads(request.data))
        db.session.add(fund)
        db.session.commit()
        return jsonify(fund)
    else:
        funds = Fund.query.filter_by(user_id=user_id).all()
        return jsonify(funds)


def _gen_token():
    token = str(uuid.uuid4())
    transactions = TransactionToken.query.filter_by(token_id=token).all()
    while transactions:
        token = str(uuid.uuid4())
        transactions = TransactionToken.query.filter_by(token_id=token).all()
    return token


@app.route("/users/<int:user_id>/transaction", methods=['POST', 'GET'])
def user_transaction(user_id):
    if request.method == 'POST':
        token = _gen_token()
        transaction_token = TransactionToken(user_id=user_id, token_id=token, used=False)
        db.session.add(transaction_token)
        db.session.commit()
        return jsonify(transaction_token)
