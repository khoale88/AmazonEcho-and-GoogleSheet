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
import time
import responses


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
#SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'
INDEX = 2
ORDERNUMBER = 1
DURATION = 0
start_time = {}


#cell = 0

app = Flask(__name__)

""""@app.before_first_request
def init_request():"""

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                'version=v4')
service = discovery.build('sheets', 'v4', http=http,
                          discoveryServiceUrl=discoveryUrl)
spreadsheetId1 = '11kcLO_td-D2lnF09GWPD99H-Ow0rZGZKw9_Fs5H5rNc'


@app.route('/', methods=['GET'])
def hello_world():
    return getMenu('crust')

@app.route('/menu/<section>', methods=['GET'])
def getMenu(section):
    """credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId1 = '11kcLO_td-D2lnF09GWPD99H-Ow0rZGZKw9_Fs5H5rNc'"""
    if section == 'crust':
        range1 = 'Menu!A2:A6'
    elif section == 'cheese':
        range1 = 'Menu!C2:C5'
    elif section == 'sauce':
        range1 = 'Menu!E2:E5'
    elif section == 'meatToppings':
        range1 = 'Menu!G2:G6'
    elif section == 'nonMeatToppings':
        range1 = 'Menu!I2:I9'
    result1 = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId1, range=range1).execute()
    values = result1.get('values', {})
    return jsonify(values)


@app.route('/order/<section>/options=<values>', methods=['POST'])
def postOrder(section, values):

    global INDEX
    value = []
    #for i in values.split("+"):

    if "No" in values:
        value.append("")
    else:
        value.append(values)


    """credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)"""

    
    #Logic to check if orderid has been generated, so as to start a new order

    #Start
    orderIndex = 'Order!A'+ '%s' % INDEX

    result1 = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId1, range=orderIndex).execute()
    values = result1.get('values', {})

    if values:
        INDEX += 1
    #End   
    
    #Based on section, identify the cellrange to populate the values
    if section == 'crust':
        rangeName = 'Order!C'+ '%s' % INDEX

    elif section == 'cheese':
        rangeName = 'Order!D'+ '%s' % INDEX

    elif section == 'sauce':
        rangeName = 'Order!E'+ '%s' % INDEX

    elif section == 'meatToppings':
        rangeName = 'Order!F'+ '%s' % INDEX

    elif section == 'nonMeatToppings':
        rangeName = 'Order!G'+ '%s' % INDEX

    elif section == 'size':
        rangeName = 'Order!H'+ '%s' % INDEX

    values = [
        value
            # Additional rows ...
        ]
    body = {
       'values': values
        }

    result = service.spreadsheets().values().update(
    spreadsheetId=spreadsheetId1, range=rangeName,
    valueInputOption="USER_ENTERED", body=body).execute()

    return jsonify(result, INDEX)


@app.route('/order/pricing', methods=['POST'])
def orderPrice():

    total = 0
    global INDEX

    """credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)"""


    rangeName = 'Order!C'+ '%s' % INDEX + ':' + 'G'+ '%s' % INDEX

    result1 = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId1, majorDimension="COLUMNS", range=rangeName).execute()

    #values = result1.get('values', {})
    options = result1["values"]

    #return jsonify(options)

    order = []
    finalorder = []

    for i in range(0, len(options)):
        if options[i]:
            if("+" in (options[i][0])):
                finalorder.append((options[i][0]).split('+'))
            else:
                order.append((options[i][0]))
            #order.append(("--".join(str(x) for x in options[i])))
        else:
            order.append("Not ordered")

    finalorder.append(order)
   # finalorder.append((s))

    #return jsonify(finalorder)

    merged = reduce(lambda x, y: x + y, finalorder)

    order = merged
    #return jsonify(order,INDEX)

    #return jsonify(options[4],INDEX)

    crustRange = 'Menu!A2:B6'
    cheeseRange = 'Menu!C2:D5'
    sauceRange = 'Menu!E2:F5'
    meatRange = 'Menu!G2:H6'
    nonMeatRange = 'Menu!I2:J9'

    range_names = [
        crustRange,cheeseRange,sauceRange,meatRange, nonMeatRange
    ]
    result1 = service.spreadsheets().values().batchGet(
        spreadsheetId=spreadsheetId1, ranges=range_names).execute()

    tee = []

    for i in range(0, len(result1["valueRanges"])):
        tee.append(result1["valueRanges"][i]["values"])

    cvs = {}


    for i in range(0, len(tee)):
        for j in range(0, len(tee[i])):
            cvs[tee[i][j][0]] = tee[i][j][1]

    cost = 0.0

    for k in order:
        for key in cvs:
            if k.lower() == key.lower():
                cost = float(str(cvs[key]))
                total += cost

    value = []
    value.append(total)

    values = [
        value
        # Additional rows ...
    ]
    body = {
        'values': values
    }

    result2 = service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId1, range='Order!J'+ '%s' % INDEX,
        valueInputOption="USER_ENTERED",body=body).execute()

    return jsonify(result2)


@app.route('/order/checkout', methods=['POST'])
def checkOutOrder():

    """credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)"""
    global ORDERNUMBER
    value = []
    value.append(ORDERNUMBER)

    body ={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {
                "range": 'Order!A' + '%s' % INDEX,
                #"majorDimension": "ROWS",
                "values": [
                    value
                    #["Item", "Wheel", "Door", "Engine"]
                ]
            },
            {
                "range": 'Order!I' + '%s' % INDEX,
                #"majorDimension": "ROWS",
                "values": [
                    ["Submitted"]
                    #["Cost", "Stocked", "Ship Date"],
                    #["$20.50", "4", "3/1/2016"]
                ]
            }
        ]
    }

    result2 = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheetId1,body=body).execute()

    global start_time

    start_time[ORDERNUMBER] = time.time()

    """from timeit import default_timer

    start = default_timer()

    # do stuff

    DURATION = default_timer() - start"""
    ORDERNUMBER += 1

    return jsonify(result2)


@app.route('/order/<int:orderid>/status', methods=['GET'])
def checkStatus(orderid):
    """credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId1 = '11kcLO_td-D2lnF09GWPD99H-Ow0rZGZKw9_Fs5H5rNc'"""
    #eturn jsonify(type(start_time[ORDERNUMBER]))
    orderIDRange = 'Order!A2:A' + '%s' % INDEX
    orderStatusRange = 'Order!I2:I' + '%s' % INDEX

    range_names = [
        orderIDRange, orderStatusRange
    ]
    result1 = service.spreadsheets().values().batchGet(
        spreadsheetId=spreadsheetId1, ranges=range_names).execute()

    # return jsonify(result1["valueRanges"])

    tee = []

    for i in range(0, len(result1["valueRanges"])):
        tee.append(result1["valueRanges"][i]["values"])

    #return jsonify(tee)

    cvs = {}

    for i in range(0, INDEX - 1):
        x = tee[0][i][0]
        y = tee[1][i][0]
        cvs[x] = y

    """for i in range(0, len(tee)):
        if len(tee[i]) > 1:
            for j in range(0, len(tee[i])):
                x = tee[0][j][0]
                y = tee[1][j][0]
                cvs[x] = y
        else:
            x = tee[0][0][0]
            y = tee[1][0][0]
            cvs[x] = y"""

    # return jsonify(cvs)

    found = False

    for key in cvs:
        if str(orderid) == key:
            found = True
            status = cvs[key]

    global start_time

    elapsed_time = time.time() - start_time[orderid]

    if elapsed_time > 0 and elapsed_time < 15:
        update = status
    elif elapsed_time > 15 and elapsed_time < 60:
        update = 'Processing'
    elif elapsed_time > 60 and elapsed_time < 120:
        update = 'Ready'
    elif elapsed_time > 120:
        update = 'Out for delivery'

    value = []
    value.append(update)

    values = [
        value
        # Additional rows ...
    ]
    body = {
        'values': values
    }

    foo = int(orderid) + 1
    result2 = service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId1, range='Order!I' + '%s' % foo,
        valueInputOption="USER_ENTERED", body=body).execute()


    if found:
        #responses.add(responses.GET,, status = 200)
        return jsonify(status)
    else:
        return jsonify("No such order !")



""""@app.route('/order/<int:orderid>/updateStatus', methods=['GET'])
def updateStatus(orderid):

    elapsed_time = time.time() - start_time
    if elapsed_time < 60:
        update = 'Processing'
    elif elapsed_time > 60 and elapsed_time < 90:
        update = 'Processed'
    elif elapsed_time > 150:
        update = 'Out for delivery'

    value = []
    value.append(update)

    values = [
        value
        # Additional rows ...
    ]
    body = {
        'values': values
    }

    foo = int(orderid) + 1
    result2 = service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId1, range='Order!I' + '%s' % foo,
        valueInputOption="USER_ENTERED", body=body).execute()

    return jsonify(result2)"""


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8082, debug=True)