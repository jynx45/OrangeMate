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
  create_order_response = _create_order(items)
  update_order_response = _update_order(create_order_response['order']['id'], email)
  add_payment_response = _add_payment_method(create_order_response['order']['id'])
  place_order_response = _place_order(create_order_response['order']['id'])

  return {
    "order_id": place_order_response['id'],
    "order_url": place_order_response['resource_uri']
  }


def _create_order(items):
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

  create_order_request = requests.post(
      CREATE_ORDER_URL, data=create_order_data)
  return json.loads(create_order_request.text)


def _update_order(order_id, email):
  update_order_data = {
    "order": {
        "email": email
    }
  }
  update_url = UPDATE_ORDER_URL.format(
    personal_token=flask_app.config['EB_TOKEN'],
    order_id=order_id,
  )
  update_order_request = requests.post(update_url, json=update_order_data)
  return json.loads(update_order_request.text)


def _add_payment_method(order_id):
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
    order_id=order_id,
  )
  payment_request = requests.post(payment_url, json=add_payment_data)
  return json.loads(payment_request.text)


def _place_order(order_id):
  place_url = PLACE_ORDER_URL.format(
    personal_token=flask_app.config['EB_TOKEN'],
    order_id=order_id,
  )
  place_order_request = requests.post(place_url)
  return json.loads(place_order_request.text)
