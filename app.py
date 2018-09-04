from flask import (
    Flask,
    jsonify,
    request,
)

app = Flask(__name__)
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
        return jsonify(user)
    else:
        users = User.query.order_by(User.username).all()
        return jsonify(users)


@app.route("/users/<int:id>", methods=['GET'])
def user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user
