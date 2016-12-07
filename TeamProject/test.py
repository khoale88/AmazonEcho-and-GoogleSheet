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
          "cheese": "no cheese",
          "meat": "Bacon, Grilled Chicken, Pepperoni",
          "crust size": "6",
          "veggies": "no veggies",
          "sauce": "Ranch",
          "quantity": 1
        }
      ],
      "AMZN ID": "amzn1.ask.account.AGX2CNUOPLHI3SAKVMAVLFZFRIQ3SHICA22Y4CZ7X244IARSTEGGAJFUH6UZVGKTIMWXP5NZXYEXA4VEF62NSJFC4NMMD7ZW6U6YLDUFY7JE4R6RUUKSCQBCIC3NAZWKUFNFPNDQ3LEKWARZR2GLCMJ57QGPRMPSWGDHHNGZYLOBVVENXP7JJPQWEZHNAOSQB2NI2HQQNHZSA3I",
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