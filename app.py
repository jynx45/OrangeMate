import json
import uuid
from datetime import datetime
from flask import (
    Flask,
    jsonify,
    request,
)
from flask_sqlalchemy import SQLAlchemy
from flask.json import JSONEncoder

app = Flask(__name__)
db = SQLAlchemy(app)
from model import (
    User,
    Fund,
    TransactionToken,
    Purchase,
)


class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        # Optional: convert datetime objects to ISO format
        try:
            return obj.isoformat()
        except Exception:

            return dict(obj)


app.json_encoder = MyJSONEncoder


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
    else:
        transactions = TransactionToken.query.filter_by(user_id=user_id).all()
        return jsonify(transactions)

@app.route("/users/<int:user_id>/transaction/<string:token>", methods=['PUT', 'GET'])
def user_transaction_check(user_id, token):
    if request.method == 'PUT':
        transaction = TransactionToken.query.filter_by(user_id=user_id, token_id=token).first()
        transaction.updated = datetime.now()
        transaction.used = True
        db.session.commit()
        return jsonify({"token_id": transaction.token_id, "used": transaction.used})
    else:
        transaction = TransactionToken.query.filter_by(user_id=user_id, token_id=token).first()
        return jsonify({"token_id": transaction.token_id, "used": transaction.used})

@app.route("/purchase", methods=['POST'])
def purchase():
    data = json.loads(request.data)
    user_id = data['user_id']
    token_id = data['transaction_token_id']
    transaction = TransactionToken.query.filter_by(user_id=user_id, token_id=token_id).first()
    if transaction and not transaction.used:
        funds = Fund.query.filter_by(user_id=user_id).all()
        prev_purchase = Purchase.query.filter_by(user_id=user_id).all()
        sum = 0
        for funding in funds:
            sum = sum + funding['amount']
        for prev_purchases in prev_purchase:
            sum = sum - prev_purchases['amount']
        if sum - data['amount'] >= 0:
            purchase = Purchase(**json.loads(request.data))
            transaction.used = True
            db.session.add(purchase)
            db.session.commit()
            return jsonify(purchase)
        else:
            return jsonify({"Error": "You have no funds to complete this purchase."})
    else:
        return jsonify({"Error": "Token does not exist or has already been used."})
