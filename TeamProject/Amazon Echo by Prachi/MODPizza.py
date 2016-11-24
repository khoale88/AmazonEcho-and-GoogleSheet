"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function


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


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Hi, Welcome to Mod Pizza, Individual Artisan-Style Pizzas, " \
                    "Please let me know in few words if you would like to place order or track existing order, " \
                    " by saying, place order or track order " 

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I did not receive a response, " \
                    "Please let me know in few words if you would like to place order or check status of existing order, " \
                    " by saying, place order or check status " 

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_pizza_size():
    session_attributes = {}
    card_title = "pizza size"
    speech_output = "You have choosen to place an order. " \
                    "Please let me know if you would like to order 6 inches or 11 inches pizza"
    reprompt_text = "I did not receive a response, " \
                    "Please let me know if you would like to order 6 inches or 11 inches pizza"                    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_pizza_sauce():
    session_attributes = {}
    card_title = "pizza sauce"
    #x = get size of pizza from handle_pizza_size
    #Read Sauce from Menu
    speech_output = "You have choosen x inches pizza. " \
                    "Please let me know which of the following sauces would you like to Add to base," \
                    "BBQ Base,"\
                    "Garlic Rub,"\
                    "Olive Oil,"\
                    "All the Above,"\
                    "No Sauce"
    reprompt_text = "I did not receive a response, " \
                    "Please let me know which of the following sauces would you like to Add to base," \
                    "BBQ Base,"\
                    "Garlic Rub,"\
                    "Olive Oil,"\
                    "All the Above,"\
                    "No Sauce"                    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_pizza_cheese():
    session_attributes = {}
    card_title = "pizza cheese"
    # x = get sauces selected from previous function
    #Read cheese from Menu
    speech_output = "You have choosen x on pizza base. " \
                    "Please let me know which of the following cheeses would you like to Add," \
                    "Mozzarella,"\
                    "Parmesan,"\
                    "Vegan Cheese,"\
                    "All the Above,"\
                    "No Cheese"
    reprompt_text = "I did not receive a response, " \
                    "Please let me know which of the following cheeses would you like to Add," \
                    "Mozzarella,"\
                    "Parmesan,"\
                    "Vegan Cheese,"\
                    "All the Above,"\
                    "No Cheese"                   
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_pizza_meat():
    session_attributes = {}
    card_title = "pizza meat"
    # x = get cheese selected from previous function
    #Read meat from Menu
    speech_output = "You have choosen x  on pizza base. " \
                    "Please let me know which of the following meat would you like to Add," \
                    "Bacon,"\
                    "Grilled Chicken,"\
                    "Pepperoni,"\
                    "All the Above,"\
                    "No Meat"
    reprompt_text = "I did not receive a response, " \
                    "Please let me know which of the following meat would you like to Add," \
                    "Bacon,"\
                    "Grilled Chicken,"\
                    "Pepperoni,"\
                    "All the Above,"\
                    "No Meat"                   
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_pizza_veggies():
    session_attributes = {}
    card_title = "pizza veggies"
    # x = get meat selected from previous function
    #Read veggies from Menu
    speech_output = "You have choosen x  on pizza base. " \
                    "Please let me know which of the following veggies would you like to Add," \
                    "Black Olives,"\
                    "Mushrooms,"\
                    "Tomato,"\
                    "All the Above,"\
                    "No veggies"
    reprompt_text = "I did not receive a response, " \
                    "Please let me know which of the following veggies would you like to Add," \
                    "Black Olives,"\
                    "Mushrooms,"\
                    "Tomato,"\
                    "All the Above,"\
                    "No veggies"                   
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_add_another_pizza():
    session_attributes = {}
    card_title = "Add another pizza"
    # y = entire order 
    speech_output = "You have ordered x pizza of size y inches, " \
                    "Do you want to add another pizza," \
                    "please respond by saying yes or no"
    reprompt_text = "I did not receive a response, " \
                    "Do you want to add another pizza," \
                    "please respond by saying yes or no"                  
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    # y = entire order 
    speech_output = "Your order is:, " \
                    "Thank you for using MOD Pizza automated pizza ordering system, " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "PlaceOrderIntent":
        return handle_pizza_size()
    if intent_name == "PizzaSizeIntent":
        return handle_pizza_sauce()
    if intent_name == "PizzaSauceIntent":
        return handle_pizza_cheese()
    if intent_name == "PizzaCheeseIntent":
        return handle_pizza_meat()
    if intent_name == "PizzaMeatIntent":
        return handle_pizza_veggies()
    if intent_name == "PizzaVeggiesIntent":
        return handle_add_another_pizza()
    if intent_name == "AddAnotherPizzaIntent":
        return handle_pizza_size()
    if intent_name == "DoNotAddPizzaIntent":
        return handle_session_end_request()
    if intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])

    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])

    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
