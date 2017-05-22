

#Intent for Adding order:

 speech_output += "If you want to add another pizza, please respond by saying,
    Add pizza, If you don't want to add pizza, please resond by saying, finish order"

    reprompt_text = "I did not receive a response, " \
                   "If you want to add another pizza, please respond by saying,
    Add pizza, If you don't want to add pizza, please resond by saying, finish order"    

#Utterance for adding order:
AddAnotherPizzaIntent Add another pizza
AddAnotherPizzaIntent Yes i would like to add another pizza
AddAnotherPizzaIntent Add pizza
AddAnotherPizzaIntent Add one pizza
AddAnotherPizzaIntent Add a pizza
AddAnotherPizzaIntent Add another pizza
AddAnotherPizzaIntent Yeah i would like to add another pizza

DoNotAddPizzaIntent finish order
DoNotAddPizzaIntent finish
DoNotAddPizzaIntent Don't add pizza
DoNotAddPizzaIntent finish ordering
DoNotAddPizzaIntent finish it



--------------------------------------------


    if intent_name == "TrackOrderIntent":
        return track_order(intent,session)
    if intent_name == "OrderIntent":
        return return_order_status(intent,session)


def track_order(intent,session):
    #crete a new order
    session_attributes = session.get('attributes',{})
    card_title = "track order"
    #initialize a menu
    if('order' not in session_attributes):  
        session_attributes = json.load(open("data_schema.json"))

    session_attributes['current_pizza'] = {}

    #instruct to size
    speech_output = "You have choosen to track an order. " \
                    "Please let me know your order number"

    reprompt_text = "I did not receive a response, " \
                     "Please let me know your order number"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def return_order_status(intent,session):
    session_attributes = session.get('attributes',{})
    card_title = 'OrderNumber'

    #take order id input
    session_attributes['order']['orderId'] = intent['slots'][card_title]['value']

    session_attributes['order'] = {}

    #return status
    speech_output = "Status of Order %s  is, "  %(session_attributes['order']['orderId'])
    speech_output += ",Thank you for choosing us"
                     
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


#Intent for tracking order:
    {
      "intent": "TrackOrderIntent"
    }, 
    {
      "intent": "OrderIntent",
      "slots":
      [
          {
            "name": "OrderNumber",
            "type": "AMAZON.NUMBER"
          }
      ]
    }, 


#Utterance:
OrderIntent {OrderNumber}



------------------------------------------------------------------------------------------------------

#List_CRUST_SIZE is still Six|Eleven

#Utterance
PizzaSizeIntent {PizzaSize} inches
PizzaSizeIntent {PizzaSize} inch