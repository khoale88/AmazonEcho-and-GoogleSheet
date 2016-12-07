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


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

