from flask import (
    Flask,
    jsonify,
    request,
)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
from model import (
    TimestampMixin,
    User,
    Fund,
    TransactionToken,
)




@app.route("/users", methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        user = User(username='admin', email='admin@example.com')
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
