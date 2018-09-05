import json
import requests
from app import app as flask_app

CREATE_ORDER_URL = "https://www.evbqaapi.com/v3/orders/?token={personal_token}".format(
    personal_token=flask_app.config['EB_TOKEN']
)
UPDATE_ORDER_URL = "https://www.evbqaapi.com/v3/orders/{order_id}/?token={personal_token}"
ADD_PAYMENT_METHOD_URL = "https://www.evbqaapi.com/v3/orders/{order_id}/payment_methods/?token={personal_token}"
PLACE_ORDER_URL = "https://www.evbqaapi.com/v3/orders/{order_id}/place/?token={personal_token}"


def create_order(email, items):
    create_order_data = {
        "event_id": 49765664442,
        "application": "manual",
    }
    tickets = []
    for item in items:
        tickets.append({
            "ticket_class_id": str(item['item_id']), "quantity": str(item['quantity'])
        })
    create_order_data['tickets'] = json.dumps(tickets)

    create_order_request = requests.post(CREATE_ORDER_URL, data=create_order_data)
    create_order_response = json.loads(create_order_request.text)

    update_order_data = {
        "order": {
            "email": email
        }
    }
    update_url = UPDATE_ORDER_URL.format(
      personal_token=flask_app.config['EB_TOKEN'],
      order_id=create_order_response['order']['id'],
    )
    update_order_request = requests.post(update_url, json=update_order_data)
    update_order_response = json.loads(update_order_request.text)

    add_payment_data = {
        "payment_methods": [
            {
                "payment_instrument_details": {
                    "instrument_type": "MANUAL"
                }
            }
        ]
    }
    payment_url = ADD_PAYMENT_METHOD_URL.format(
      personal_token=flask_app.config['EB_TOKEN'],
      order_id=create_order_response['order']['id'],
    )
    payment_request = requests.post(payment_url, json=add_payment_data)

    place_url = PLACE_ORDER_URL.format(
      personal_token=flask_app.config['EB_TOKEN'],
      order_id=create_order_response['order']['id'],
    )
    place_order_request = requests.post(place_url)
    place_order_response = json.loads(place_order_request.text)

    return place_order_response