"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
from pizza_functions import build_response, build_speechlet_response,getMenu,postOrder,getOrderStatus,autoOrderStatus
import json
    
# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}

    card_title = "Welcome"
    speech_output = "Hi, Welcome to Pizza ordering system, " \
                    "Please let me know in few words if you would like to place order or track existing order, " \
                    " by saying, place order, or, track order. " 

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I did not receive a response, " \
                    "Please let me know in few words if you would like to place order or check status of existing order, " \
                    " by saying, place order, or, check status. " 

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_place_order(intent,session):
    #crete a new order
    session_attributes = session.get('attributes',{})
    card_title = "order a pizza"
    #initialize a menu
    if('order' not in session_attributes):  
        session_attributes = json.load(open("data_schema.json"))

    del session_attributes['current_pizza']
    session_attributes['current_pizza'] = {}

    #instruct to sauce
    #only get sauce if it is the 1st time in this session - not yet in the menu
    if('crust size' not in session_attributes['menu']):
        session_attributes['menu']['crust size'] = {}
        session_attributes['menu']['crust size'] = getMenu('crust')   

    crust_speech =  "Please let me know which crust size would like to order, "
    for cr in session_attributes['menu']['crust size']:
        crust_speech += "%s inches for %s dollar, " %(cr['name'],cr['price'])

    #instruct to size
    speech_output = "You have choosen to place an order. " + crust_speech
                    
    reprompt_text = "I did not receive a response, " +crust_speech

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_pizza_size(intent,session):
    session_attributes = session.get('attributes',{})
    card_title = 'PizzaSize'

    #check if a pizza goes through welcome - previous step
    if 'current_pizza' not in session_attributes:
        return handle_place_order(intent,session)

    #forced back
    if  card_title not in intent['slots']:
        # and not goes through welcome
        if 'crust size' not in session_attributes['current_pizza']:
            return handle_place_order(intent,session)
    else:
        #get pizza size
        size = intent['slots'][card_title]['value']
        #check valid size
        if size not in ['6','11']:
            return handle_place_order(intent,session)
        #update pizza size
        session_attributes['current_pizza']['crust size'] = size

    #instruct to sauce
    #only get sauce if it is the 1st time in this session - not yet in the menu
    if('sauce' not in session_attributes['menu']):
        session_attributes['menu']['sauce'] = {}
        session_attributes['menu']['sauce'] = getMenu('sauce')
    
    #build sauce speech
    sauce_speech = "Please let me know which of the following sauces would you like to Add to base, "
    for s in session_attributes['menu']['sauce']:
        sauce_speech += "%s for %s dollar, " %(str(s['name']),str(s['price']))
    sauce_speech +=  "all sauce, or no sauce, "
    
    #build output
    speech_output = "You have choosen pizza of %s inches. " %(session_attributes['current_pizza']['crust size'])
    speech_output += sauce_speech

    reprompt_text = "I did not receive a response, " 
    reprompt_text += sauce_speech          

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_pizza_sauce(intent,session):
    session_attributes = session.get('attributes',{})
    card_title = 'PizzaSauce'

    #check if a pizza goes through size - previous step
    if('current_pizza' not in session_attributes or
        'crust size' not in session_attributes['current_pizza']):
        return handle_pizza_size(intent,session)

    #force
    if card_title not in intent['slots']:
        if 'sauce' not in session_attributes['current_pizza']:
            return handle_pizza_size(intent,session)
    else:
        #get sauce out
        sauce_response = intent['slots'][card_title]['value']
        #add sauce  
        if ('no sauce' in sauce_response.lower()):
            selected_sauce = 'no sauce'
        elif ('all sauce' in sauce_response.lower()):
            selected_sauce = ', '.join(s['name'] for s in session_attributes['menu']['sauce'])
        else:
            selected_sauce = ', '.join(s['name'] for s in session_attributes['menu']['sauce'] 
                                                if s['name'].lower() in sauce_response.lower())
        session_attributes['current_pizza']['sauce'] = selected_sauce

    #instruct to cheese
    #only get chees if it is not in the menu
    if('cheese' not in session_attributes['menu']):
        session_attributes['menu']['cheese'] = {}
        session_attributes['menu']['cheese'] = getMenu('cheese')

    #cheese speech, need to add all cheese?
    cheese_speech = "Please let me know which of the following cheeses would you like to Add, "
    for c in session_attributes['menu']['cheese']:
        cheese_speech += "%s for %s dollar, " %(str(c['name']),str(c['price']))
    cheese_speech += "All cheese, or no cheese, "

    #build output
    speech_output = "You have choosen %s on pizza base. " %(session_attributes['current_pizza']['sauce'])
    speech_output += cheese_speech

    reprompt_text = "I did not receive a response, " 
    reprompt_text += cheese_speech

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_pizza_cheese(intent,session):
    session_attributes = session.get('attributes',{})
    card_title = 'PizzaCheese'

    #check if a pizza goes through sauce - previous step
    if('current_pizza' not in session_attributes or
        'sauce' not in session_attributes['current_pizza']):
        return handle_pizza_sauce(intent,session)

    if card_title not in intent['slots']:
        if 'cheese' not in session_attributes['current_pizza']:
            return handle_pizza_sauce(intent,session)
    else:
        #get the cheese out
        cheese_response = intent['slots'][card_title]['value']
        #add cheese  
        if ('no cheese' in cheese_response.lower()):
            selected_cheese = 'no cheese'
        elif ('all cheese' in cheese_response.lower()):
            selected_cheese = ', '.join(c['name'] for c in session_attributes['menu']['cheese'])
        else:
            selected_cheese = ', '.join(c['name'] for c in session_attributes['menu']['cheese'] 
                                                if c['name'].lower() in cheese_response.lower())
        session_attributes['current_pizza']['cheese'] = selected_cheese

    #instruct to meat
    #only get meat if it is not in the menu
    if('meat' not in session_attributes['menu']):
        session_attributes['menu']['meat'] = {}
        session_attributes['menu']['meat'] = getMenu('meat')

    #build meat speech
    meat_speech = "Please let me know which of the following meat would you like to Add, "
    for m in session_attributes['menu']['meat']:
        meat_speech += "%s for %s dollar, " %(str(m['name']),str(m['price']))
    meat_speech += "all meat, or no meat, "

    #build output
    speech_output = "You have choosen %s  on pizza base. " %(session_attributes['current_pizza']['cheese'])
    speech_output += meat_speech
                     
    reprompt_text = "I did not receive a response, " 
    reprompt_text += meat_speech

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_pizza_meat(intent,session):
    session_attributes = session.get('attributes',{})
    card_title = 'PizzaMeat'
    #check if a pizza goes through cheese - previous step
    if('current_pizza' not in session_attributes or 
        'cheese' not in session_attributes['current_pizza']):
        return handle_pizza_cheese(intent,session)

    if card_title not in intent['slots']:
        if 'meat' not in session_attributes['current_pizza']:
            return handle_pizza_cheese(intent,session)
    else:
        #get the meat out
        meat_response = intent['slots'][card_title]['value']
        #update meat 
        if ('no meat' in meat_response.lower()):
            selected_meat = 'no meat'
        elif ('all meat' in meat_response.lower()):
            selected_meat = ', '.join(m['name'] for m in session_attributes['menu']['meat'])
        else:
            selected_meat = ', '.join(m['name'] for m in session_attributes['menu']['meat']
                                                if m['name'].lower() in meat_response.lower())
        session_attributes['current_pizza']['meat'] = selected_meat

    #instruct to veggies
    #only get veggies if it is not in the menu
    if('veggies' not in session_attributes['menu']):
        session_attributes['menu']['veggies'] = {}
        session_attributes['menu']['veggies'] = getMenu('veggies')

    #build veggies instructions
    veggies_speech = "Please let me know which of the following veggies would you like to Add, "
    for v in session_attributes['menu']['veggies']:
        veggies_speech += "%s for %s dollar, " %(str(v['name']),str(v['price']))
    veggies_speech += "all veggies, or no veggies"

    #build output
    speech_output = "You have choosen %s  on pizza base. " %(session_attributes['current_pizza']['meat'])
    speech_output += veggies_speech

    reprompt_text = "I did not receive a response, "
    reprompt_text += veggies_speech

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_pizza_veggies(intent,session):
    session_attributes = session.get('attributes',{})
    card_title = 'PizzaVeggies'

    #check if a pizza goes through meat - previous step
    if('current_pizza' not in session_attributes or
        'meat' not in session_attributes['current_pizza']):
        return handle_pizza_meat(intent,session)

    #get the veggies out
    if card_title not in intent['slots']:
        if 'veggies' not in session_attributes['current_pizza']:
            return handle_pizza_meat(intent,session)
    else:
        veggies_response = intent['slots'][card_title]['value']
        #update veggies
        if ('no veggies' in veggies_response.lower()):
            selected_veggies = 'no veggies'
        elif ('all veggies' in veggies_response.lower()):
            selected_veggies = ', '.join(v['name'] for v in session_attributes['menu']['veggies'])
        else:
            selected_veggies = ', '.join(v['name'] for v in session_attributes['menu']['veggies']
                                                if v['name'].lower() in veggies_response.lower())
        session_attributes['current_pizza']['veggies'] = selected_veggies

    #add quantity for testing
    session_attributes['current_pizza']['quantity'] = 1

    #finish this pizza
    current_pizza = session_attributes['current_pizza']
    pizzas = session_attributes['order']['pizzas']
    pizzas.append(session_attributes['current_pizza'])

    #instruct to next
    speech_output = "You have choosen %s on pizza base. " %(session_attributes['current_pizza']['veggies'])
    speech_output += "If you want to add another pizza, please respond by saying, Add pizza, "\
                     "If you don't want to add pizza, please resond by saying, finish order"

    reprompt_text = "I did not receive a response, " \
                    "If you want to add another pizza, please respond by saying, Add pizza, "\
                    "If you don't want to add pizza, please resond by saying, finish order." 

    #del session_attributes['current_pizza']
    #session_attributes['current_pizza'] = {}

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_do_not_add(intent,session):
    session_attributes = session.get('attributes',{})
    #guard to make sure at least one pizza is complete
    if('current_pizza' not in session_attributes or
    'veggies' not in session_attributes['current_pizza']):
        return handle_pizza_veggies(intent, session)
    card_title = "DoNotAddPizza"
    
    speech_output = "May I have your name and address before we place your order?"\
                    "you can just speak your address without name"
    reprompt_text = "I'm waiting for your name and address!"\
                    'you can just speak your address without name'
    # Setting this to true ends the session and exits the skill.
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_customer(intent,session):
    session_attributes = session.get('attributes',{})
    #guard to make sure at least one pizza is complete
    if('current_pizza' not in session_attributes or
    'veggies' not in session_attributes['current_pizza']):
        return handle_pizza_veggies(intent, session)

    if intent['name'] == 'CustomerName':
        return handle_name(intent,session)
    if intent['name'] == 'Customerdetails':
        return handle_address(intent,session)

def handle_name(intent,session):
    session_attributes = session.get('attributes',{})
    card_title = "CustomerName"

    name = intent['slots']['CustName']['value']
    session_attributes['order']['customer']['name'] = name
    
    speech_output = "Hi %s, now tell me your address, we will deliver the pizza to you" %(session_attributes['order']['customer']['name'])
                    
    reprompt_text = "I'm waiting for your address"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_address(intent,session):
    session_attributes = session.get('attributes',{})
    card_title = "CustomerAddress"

    addr = ""
    for slot in ['CustAddress', 'CustStreet', 'City']:
        if 'value' in intent['slots'][slot]:
            addr += intent['slots'][slot]['value']
    session_attributes['order']['customer']['address'] = addr
    #check if valid city
    if 'value' in intent['slots']['City']:
        return finish_order(intent,session)
    
    #invalid
    speech_output = "please input a valid address with valid city!"\
                    "What is your address again?"
    reprompt_text = "I'm waiting for your address"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def finish_order(intent,session):
    session_attributes = session.get('attributes',{})
    card_title = "PostOrder"

    size = 0
    pizzas_speech = ""
    for pizza in session_attributes['order']['pizzas'] :
        size += int(pizza['quantity'])
        #quantity, size, sauce, cheese, meat, veggies
        pizzas_speech += " %s of %s inch pizza with %s, %s, %s, %s."\
                            %(pizza['quantity'],pizza['crust size'],pizza['sauce'],pizza['cheese'],pizza['meat'],pizza['veggies'])
    
    user = session.get('user',{})
    session_attributes['order']['AMZN ID'] = user.get('userId','')

    order = json.loads(postOrder(session_attributes['order']))
    orderId = order['orderId']
    price = order['price']
    dollar = int(price)
    cents = int((price - dollar)*100)

    #post order, get order ID and price
    speech_output = ""
    if session_attributes['order']['customer']['name'] != "":
        speech_output += "Hi %s, "%(session_attributes['order']['customer']['name'])
    speech_output += "You have ordered total of %d pizza."%(size)
    speech_output += pizzas_speech
    speech_output +="Your order number is: %d. " %(int(orderId))
    speech_output +="Your order price is %d dollars and %d cents. " %(dollar,cents)
    speech_output +="Thank you for using our Pizza ordering system, " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def handle_add(intent,session):
    #crete a new order
    session_attributes = session.get('attributes',{})
    card_title = "Add Another"
    #initialize a menu
    if('order' not in session_attributes):  
        return handle_place_order(intent,session)

    del session_attributes['current_pizza']
    session_attributes['current_pizza'] = {}

    crust_speech =  "Please let me know which crust size would like to order, "
    for cr in session_attributes['menu']['crust size']:
        crust_speech += "%s inches for %s dollar" %(cr['name'],cr['price'])

    #instruct to size
    speech_output = "You have choosen to add another pizza. " + crust_speech
                    
    reprompt_text = "I did not receive a response, " +crust_speech

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))    


def handle_session_end_request(intent, session):
    session_attributes = session.get('attributes',{})
    card_title = "EndSession"

    cancel_speech = ""
    if 'order' in session_attributes:
        cancel_speech = "you have chosen to stop your order, your order will not be placed. "

    speech_output =cancel_speech + "Thank you for using our pizza ordering system, " \
                    "Have a nice day! "
    

    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def track_order(intent,session):
    #crete a new order
    session_attributes = session.get('attributes',{})
    card_title = "track order"
    #initialize a menu
    if('order' not in session_attributes):  
        session_attributes = json.load(open("data_schema.json"))

    session_attributes['current_pizza'] = {}

    user = session.get('user',{})
    AMZNId = user.get('userId','')
    status = autoOrderStatus(AMZNId)
    if len(status) == 0:
        speech_output = "We found 0 order associated with your Amazon Account. " \
                        "Please let me know your order number in format by saying, track order number example, track ten"

        reprompt_text = "I did not receive a response, " \
                        "Please let me know your order number by saying, track order number example, track ten"

        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))
    else:
        status_speech = "We found %d orders. " %(len(status))
        for stt in status:
            status_speech += "Status of Order %d  is %s, "  %(int(stt[0]),stt[1])
        speech_output = status_speech + "Thank you for choosing us!"
        
        reprompt_text = None
                        
        should_end_session = True
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))


def return_order_status(intent,session):
    session_attributes = session.get('attributes',{})
    card_title = 'OrderNumber'

    #take order id input
    orderIds = intent['slots'][card_title]['value'].split(" ")

    status = getOrderStatus(orderIds)
    #return status
    speech_output = "We found %d orders. " %(len(status))
    for stt in status:
        speech_output += "Status of Order %d  is %s, "  %(stt['orderId'],stt['status'])
    
    speech_output += "Thank you for choosing us!"
    
    reprompt_text = None
                     
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

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
        return handle_place_order(intent,session)
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
        return handle_add(intent,session)
    if intent_name == "DoNotAddPizzaIntent":
        return handle_do_not_add(intent,session)
    if intent_name == "Customerdetails" or intent_name == "CustomerName":
        return handle_customer(intent,session)
    if (intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent" or 
        intent_name == "CancelIntent"):
        return handle_session_end_request(intent, session)
    if intent_name == "TrackOrderIntent":
        return track_order(intent,session)
    if intent_name == "OrderIntent":
        return return_order_status(intent,session)
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
