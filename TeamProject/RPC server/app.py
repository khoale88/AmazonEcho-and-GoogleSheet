#!/usr/bin/env python
 
from __future__ import print_function
from flask import Flask,jsonify,request,json
#from models import db,Expense,CreateDB

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials
import time
import responses



try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
INDEX = 2
TRACK = 2
ORDERNUMBER = 1
start_time = {}

app = Flask(__name__)

credentials = ServiceAccountCredentials.from_json_keyfile_name('MyPizza.json', SCOPES)
http = credentials.authorize(httplib2.Http())
discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
service = discovery.build('sheets', 'v4', http=http,discoveryServiceUrl=discoveryUrl)
googleSheetId = '11kcLO_td-D2lnF09GWPD99H-Ow0rZGZKw9_Fs5H5rNc'


@app.route('/', methods=['GET'])
def hello_world():
    return getMenu('crust')

@app.route('/menu/<section>', methods=['GET'])
def getMenu(section):
    if section == 'crust':
        range1 = 'Menu!A2:B3'
    elif section == 'cheese':
        range1 = 'Menu!C2:D4'
    elif section == 'sauce':
        range1 = 'Menu!E2:F4'
    elif section == 'meat':
        range1 = 'Menu!G2:H4'
    elif section == 'veggies':
        range1 = 'Menu!I2:J4'
    menuResult = service.spreadsheets().values().get(spreadsheetId=googleSheetId, range=range1).execute()
    values = menuResult.get('values', {})
    return jsonify(values)


@app.route('/order', methods=['POST'])
def post():

    global INDEX
    totalPrice = 0
    value = []
    data = json.loads(request.data)
    pizzas = data["pizzas"]
    customer = data["customer"]

    for pizza in pizzas:
        value = []

        value.append(pizza["crust size"])
        value.append(pizza["cheese"])
        value.append(pizza["sauce"])
        value.append(pizza["meat"])
        value.append(pizza["veggies"])
        value.append(pizza["quantity"])

        #Push Order to sheet

        rangeName = 'Order!C' + '%s' % INDEX + ':' + 'H' + '%s' % INDEX

        result = service.spreadsheets().values().update(spreadsheetId=googleSheetId, range=rangeName,
            valueInputOption="USER_ENTERED", body={'values': [value]}).execute()

        #Push Price to sheet
        totalPrice += orderPrice(pizza["quantity"])

        INDEX += 1

    values = []

    for n in range(0, len(pizzas)):
        values.append([ORDERNUMBER])

    saveOrderId(len(pizzas), data["AMZN ID"], customer["name"], customer["phone_number"], customer["address"])

    start = INDEX - len(pizzas)
    end = INDEX -1

    range2 = 'Order!A' + '%s' % start + ':' + 'A' + '%s' % end

    result = service.spreadsheets().values().update(spreadsheetId=googleSheetId, range=range2,
        valueInputOption="USER_ENTERED", body={'values': values}).execute()

    return jsonify({"orderId": ORDERNUMBER-1, "price": totalPrice})

def orderPrice(quantity):

    total = 0

    rangeName = 'Order!C'+ '%s' % INDEX + ':' + 'H'+ '%s' % INDEX

    result1 = service.spreadsheets().values().get(
        spreadsheetId=googleSheetId, majorDimension="COLUMNS", range=rangeName).execute()

    options = result1["values"]

    order = []
    finalorder = []

    for i in range(0, len(options)):
        if options[i]:
            if(", " in (options[i][0])):
                finalorder.append((options[i][0]).split(', '))
            else:
                order.append((options[i][0]))
        else:
            order.append("Not ordered")

    finalorder.append(order)


    merged = reduce(lambda x, y: x + y, finalorder)

    order = merged

    crustRange = 'Menu!A2:B6'
    cheeseRange = 'Menu!C2:D5'
    sauceRange = 'Menu!E2:F5'
    meatRange = 'Menu!G2:H6'
    nonMeatRange = 'Menu!I2:J9'

    range_names = [
        crustRange,cheeseRange,sauceRange,meatRange, nonMeatRange
    ]
    result1 = service.spreadsheets().values().batchGet(
        spreadsheetId=googleSheetId, ranges=range_names).execute()

    tee = []

    for i in range(0, len(result1["valueRanges"])):
        tee.append(result1["valueRanges"][i]["values"])

    cvs = {}


    for i in range(0, len(tee)):
        for j in range(0, len(tee[i])):
            cvs[tee[i][j][0]] = tee[i][j][1]

    cost = 0

    for k in order:
        for key in cvs:
            if k.lower() == key.lower():
                cost = int(str(cvs[key]))
                total += cost
    
    total = total * int(quantity)
    value = []
    value.append(total)

    values = [
        value
    ]
    body = {
        'values': values
    }

    result2 = service.spreadsheets().values().update(
        spreadsheetId=googleSheetId, range='Order!J'+ '%s' % INDEX,
        valueInputOption="USER_ENTERED",body=body).execute()

    return total


def saveOrderId(length, amazonId, customerName, phoneNumber, address):
    start = INDEX - length
    end = INDEX -1

    range1 = 'Order!J' + '%s' % start + ':' + 'J' + '%s' % end
    result1 = service.spreadsheets().values().get(spreadsheetId=googleSheetId, range=range1).execute()

    total = 0

    for i in result1["values"]:
        total += int(i[0])

    global ORDERNUMBER, TRACK

    value = []

    value.append(ORDERNUMBER)
    value.append(amazonId)
    value.append("Submitted")
    value.append(total)
    value.append(customerName)
    value.append(phoneNumber)
    value.append(address)

    rangeName = 'Track!A' + '%s' % TRACK + ':' + 'G' + '%s' % TRACK

    result = service.spreadsheets().values().update(spreadsheetId=googleSheetId, range=rangeName,
            valueInputOption="USER_ENTERED", body={'values': [value]}).execute()

    global start_time

    start_time[ORDERNUMBER] = time.time()

    ORDERNUMBER += 1
    TRACK += 1

    return jsonify(result)


@app.route('/order/<int:orderid>/status', methods=['GET'])
def checkStatus(orderid):    
    orderIDRange = 'Track!A2:A' + '%s' % TRACK
    orderStatusRange = 'Track!C2:C' + '%s' % TRACK

    if(orderid >= ORDERNUMBER):
        return jsonify({"error": "Order Id not found"}), 404

    range_names = [
        orderIDRange, orderStatusRange
    ]

    allOrders = service.spreadsheets().values().batchGet(
        spreadsheetId=googleSheetId, ranges=range_names).execute()

    orderIds = []

    orderIds.append(allOrders["valueRanges"][0]["values"])

    count = 1
    for order in orderIds[0]:
        count += 1
        if str(orderid) == order[0][0]:
            break

    status = allOrders["valueRanges"][1]["values"][count-1][0]

    elapsed_time = time.time() - start_time[orderid]

    if elapsed_time > 0 and elapsed_time < 60:
        update = status
    elif elapsed_time > 60 and elapsed_time < 180:
        update = 'Processing'
    elif elapsed_time > 180 and elapsed_time < 600:
        update = 'Ready'
    elif elapsed_time > 600 and elapsed_time < 900:
        update = 'Out for delivery'
    elif elapsed_time > 900:
        update = 'Delivered'

    foo = int(orderid) + 1
    updateOrder = service.spreadsheets().values().update(
        spreadsheetId=googleSheetId, range='Track!C' + '%s' % foo,
        valueInputOption="USER_ENTERED", body={'values': [[update]]}).execute()

    if status != "":
        return jsonify({"status": update})

    return jsonify({"error": "Order not found"}), 404

@app.route('/orders/<string:amazonId>', methods=['GET'])
def getOrdersAmazonId(amazonId):
    searchResult = []
    if(TRACK == 2):
        return jsonify({"error": "No orders"})
    orderIDRange = 'Track!A2:D' + '%s' % (TRACK - 1)

    range_names = [
        orderIDRange
    ]

    allOrders = service.spreadsheets().values().batchGet(
        spreadsheetId=googleSheetId, ranges=range_names).execute()

    orderIds = []

    orderIds.append(allOrders["valueRanges"][0]["values"])
    for order in orderIds[0]:
        if order[1] == str(amazonId) and order[2] != "Delivered":
            searchResult.append(order)

    if len(searchResult) > 0:
        return jsonify({"orders": searchResult})

    return jsonify({"error": "Order not found"}), 404


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8082, debug=True)