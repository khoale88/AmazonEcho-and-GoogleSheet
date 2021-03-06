import requests
import json


# --------------Helper that help to get menu items---------------------------
host = "http://35.164.41.209:8082"
#host = '"http://localhost:8082'
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

ids = [1]
def getOrderStatus(orderIds):
  status = []
  for orderId in orderIds:
    endpoint = '/order/%s/status'%(orderId)
    r = requests.get(url = host+endpoint)
    print 'check order 1'
    print '#################raw input##############'
    print r
    print r.content
    if r.status_code == 200:
      print '#############status 200################'
      print r.content
      st = {}
      st['orderId'] = orderId
      st['status'] = str(json.loads(r.content)['status'])
      status.append(st)
  return status

def autoOrderStatus(AMZNId):
  endpoint = '/orders/%s'%(AMZNId)
  r = requests.get(url = host+endpoint)
  result = []
  print 'check AMZN ID'
  print '==============raw input================='
  print r
  print r.content
  if r.status_code == 200:
    print '==============status 200================='
    print r.content
    for orderStatus in json.loads(r.content)['orders']:
      if orderStatus[2] != 'delivered':
        result.append([str(orderStatus[x]) for x in [0,2]])
  return result


print ("\n\n###########ORDER ID##############")
print getOrderStatus(ids)
print ('\n\n')
print ("============AMZN ID==============")
print autoOrderStatus(data["AMZN ID"])



