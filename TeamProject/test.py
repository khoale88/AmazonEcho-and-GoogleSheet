import requests
import json


# --------------Helper that help to get menu items---------------------------
host = "http://35.164.41.209:8082"

def getMenu(section):
    endpoint = "/menu/"+section
    r = requests.get(url = host+endpoint)
    if r.status_code == 200:
        output = []
        s = json.loads(r.content)
        for sublist in s:
            item = {}
            item['name'] = str(sublist[0])
            item['price'] = str(sublist[1])
            output.append(item)
        return output

data = {
      "customer": {
        "phone_number": "",
        "name": ""
      },
      "pizzas": [
        {
          "cheese": "Mozzarella, Parmesan, Vegan Cheese",
          "meat": "Bacon, Grilled Chicken, Pepperoni",
          "crust size": "6",
          "veggies": "Black Olives, Mushrooms, Tomato",
          "sauce": "Ranch, Garlic Rub, Olive Oil",
          "quantity": 1
        },
        {
          "cheese": "no cheese",
          "meat": "no meat",
          "crust size": "11",
          "veggies": "no veggies",
          "sauce": "no sauce",
          "quantity": 1
        }
      ],
      "AMZN ID": "",
      "order ID": ""
    }

def postOrder(order):
    for pizza in order['pizzas']:
      for key in ('cheese','meat','crust size','veggies','sauce'):
        if 'no' in pizza[key]:
          pizza[key] = ''
    print order
    endpoint = "/order"
    r = requests.post(url = host+endpoint, json = order)
    print r.status_code
    print r.content

postOrder(data)