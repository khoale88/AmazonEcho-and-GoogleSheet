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

app = Flask(__name__)

"""@app.before_first_request
def init_request():
	CreateDB()
	db.create_all()	"""

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


@app.route('/menu/<section>', methods=['GET'])
def getMenu(section):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId1 = '11kcLO_td-D2lnF09GWPD99H-Ow0rZGZKw9_Fs5H5rNc'
    if section == 'crust':
        range1 = 'Menu!A2:A6'
    elif section == 'cheese':
        range1 = 'Menu!B2:B5'
    elif section == 'sauce':
        range1 = 'Menu!C2:C5'
    elif section == 'meatToppings':
        range1 = 'Menu!D2:D6'
    elif section == 'nonMeatToppings':
        range1 = 'Menu!E2:E8'
    result1 = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId1, range=range1).execute()
    values = result1.get('values', {})
    return jsonify(values)


    
@app.route('/order/<section>/options=<values>', methods=['POST'])
def postOrder(section, values):

    global INDEX
    value = []
    #for i in values.split("+"):
    value.append(values)

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    orderIndex = 'Order!A'+ '%s' % INDEX
    result1 = service.spreadsheets().values().get(
        spreadsheetId='11kcLO_td-D2lnF09GWPD99H-Ow0rZGZKw9_Fs5H5rNc', range=orderIndex).execute()
    values = result1.get('values', {})

    if values:
        INDEX += 1
    
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
    spreadsheetId='11kcLO_td-D2lnF09GWPD99H-Ow0rZGZKw9_Fs5H5rNc', range=rangeName,
    valueInputOption="USER_ENTERED", body=body).execute()

    return jsonify(result)


@app.route('/order/<int:expense_id>', methods=['GET','PUT','DELETE'])
def getExpense(expense_id):
	if(request.method == 'GET'):
		getExpense = Expense.query.filter_by(id =expense_id).first_or_404()
		return jsonify(getExpense.serialize)
	
	elif(request.method == 'DELETE'):
		deleteExpense = Expense.query.filter_by(id = expense_id).first_or_404()
		db.session.delete(deleteExpense)
		db.session.commit()
		resp = jsonify({'Status' : 'True'})
		resp.status_code = 204
		return resp

	else:
		putExpense = Expense.query.filter_by(id = expense_id).first_or_404()
		req = request.get_json(force=True)

		putExpense.estimated_costs = req['estimated_costs']
		#Code for any field update:
		#for key in request.json:
		#		putExpense.setKey(key,request.json[key])
		db.session.commit()
		resp = jsonify({'Status' : 'True'})
		resp.status_code = 202
		return resp


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8082, debug=True)