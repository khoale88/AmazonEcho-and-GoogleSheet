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

def get_welcome_response(session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}

    card_title = "Welcome"
    speech_output = "Hi, Welcome to Mod Pizza, Individual Artisan-Style Pizzas, " \
                    "Please let me know in few words if you would like to place order or track existing order, " \
                    " by saying, place order, or, track order " 

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I did not receive a response, " \
                    "Please let me know in few words if you would like to place order or check status of existing order, " \
                    " by saying, place order, or, check status " 

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_place_order(session):
    #crete a new order
    session_attributes = {}
    card_title = "order a pizza"

    #instruct to size
    speech_output = "You have choosen to place an order. " \
                    "Please let me know if you would like to order 6 inches or 11 inches pizza"
    reprompt_text = "I did not receive a response, " \
                    "Please let me know if you would like to order 6 inches or 11 inches pizza"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_pizza_size(intent,session):
    session_attributes = session.get('attributes',{})
    card_title = 'PizzaSize'
    size = intent['slots'][card_title]['value']
    if('current_pizza' not in session_attributes):
        session_attributes["current_pizza"] = {}
    #also need to check if size is correct!!!!!!!!!!!!!!!!!!!!!!!!!!
    current_pizza = session_attributes['current_pizza']
    current_pizza[card_title] = size
    #create a new pizza with new size
    session_attributes['current_pizza']=current_pizza

    
    #instruct to sauce
    speech_output = "You have choosen %s inches pizza. " \
                    "Please let me know which of the following sauces would you like to Add to base," \
                    "BBQ Base,"\
                    "Garlic Rub,"\
                    "Olive Oil,"\
                    "All the Above,"\
                    "No Sauce"%(size)

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

def handle_pizza_sauce(intent,session):
    session_attributes = session.get('attributes',{})
    card_title = 'PizzaSauce'

    #get the sauce out
    response = intent['slots'][card_title]['value']

    menu = ['garlic rub','Olive Oil','bbq base']    
    #add sauce
    lst = [m for m in menu if m.lower() in response.lower()] 
    current_pizza =  session_attributes['current_pizza']
    current_pizza[card_title] = lst
    session_attributes['current_pizza'] = current_pizza

    #instruct to cheese
    #Read Sauce from Menu
    speech_output = "You have choosen %s on pizza base. " \
                    "Please let me know which of the following cheeses would you like to Add," \
                    "Mozzarella,"\
                    "Parmesan,"\
                    "Vegan Cheese,"\
                    "All the Above,"\
                    "No Cheese" %(', '.join(lst))
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

def handle_pizza_cheese(intent,session):
    session_attributes = session.get('attributes',{})
    card_title = 'PizzaCheese'

    #get the sauce out
    response = intent['slots'][card_title]['value']

    menu = ['Mozzarella','Parmesan','vegan chsses']    
    #add 
    lst = [m for m in menu if m.lower() in response.lower()]
    session_attributes['current_pizza'][card_title] = lst

    #Read cheese from Menu
    #instruct to meat
    speech_output = "You have choosen %s  on pizza base. " \
                    "Please let me know which of the following meat would you like to Add," \
                    "Bacon,"\
                    "Grilled Chicken,"\
                    "Pepperoni,"\
                    "All the Above,"\
                    "No Meat"%(', '.join(lst))
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

def handle_pizza_meat(intent,session):
    session_attributes = session.get('attributes',{})
    card_title = 'PizzaMeat'

    #get the sauce out
    response = intent['slots'][card_title]['value']

    menu = ['bacon','gilled chicken','pepperoni']    
    #add
    lst = [m for m in menu if m.lower() in response.lower()]
    session_attributes['current_pizza'][card_title] = lst

    # instruc to next ingredient
    #Read meat from Menu
    speech_output = "You have choosen %s  on pizza base. " \
                    "Please let me know which of the following veggies would you like to Add," \
                    "Black Olives,"\
                    "Mushrooms,"\
                    "Tomato,"\
                    "All the Above,"\
                    "No veggies"%(', '.join(lst))
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

def handle_pizza_veggies(intent,session):
    session_attributes = session.get('attributes',{})
    card_title = 'PizzaVeggies'

    #get the sauce out
    response = intent['slots'][card_title]['value']

    menu = ["Black Olives","Mushrooms","Tomato"]    
    #add 
    lst = [m for m in menu if m.lower() in response.lower()]
    session_attributes['current_pizza'][card_title] = lst

    #finish this pizza
    if'order' not in session_attributes:
        session_attributes['order'] = []
    order = session_attributes['order']
    order.append(session_attributes['current_pizza'])
    session_attributes['order'] = order
    #what if I want to order more of this?


    #instruct to next
    #Read veggies from Menu
    speech_output = "You have choosen %s on pizza base. " \
                    "do you want to add another pizza?"%(', '.join(lst))
    reprompt_text = "I did not receive a response, " \
                    "Do you want to add another pizza?"                 
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request(session):
    card_title = "Session Ended"
    size = len(session['attributes']['order'])
    # y = entire order 
    speech_output = "You have order %s pizza,"\
                    "Your order number is: 1234," \
                    "Thank you for using MOD Pizza automated pizza ordering system, " \
                    "Have a nice day! "%(size)
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
    
    return get_welcome_response(session)


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "PlaceOrderIntent":
        return handle_place_order(session)
    if intent_name == "PizzaSizeIntent":
        return handle_pizza_size(intent,session)
    if intent_name == "PizzaSauceIntent":
        return handle_pizza_sauce(intent,session)
    if intent_name == "PizzaCheeseIntent":
        return handle_pizza_cheese(intent,session)
    if intent_name == "PizzaMeatIntent":
        return handle_pizza_meat(intent,session)
    if intent_name == "PizzaVeggiesIntent":
        return handle_pizza_veggies(intent,session)
    if intent_name == "AddAnotherPizzaIntent":
        return handle_pizza_size(intent,session)
    if intent_name == "DoNotAddPizzaIntent":
        return handle_session_end_request(session)
    if intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request(session)
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
