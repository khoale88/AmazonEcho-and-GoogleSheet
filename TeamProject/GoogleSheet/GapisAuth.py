import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://spreadsheets.google.com/feeds']

"""
    get out the sheet
"""
def login_open_sheet(sheetname):
    credentials = ServiceAccountCredentials.from_json_keyfile_name('MyPizza-3b4068900e99.json',SCOPES)
    gss_client=gspread.authorize(credentials)
    gss=gss_client.open(sheetname)
    return gss
    #worksheet = gss.sheet1
    #return worksheet
