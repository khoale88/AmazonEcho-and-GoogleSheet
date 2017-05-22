    {
      "intent": "Customerdetails",
      "slots":
      [
          {
            "name": "CustName",
            "type": "AMAZON.US_FIRST_NAME"
          }
      ]
    },   
 {
      "intent": "CustomerCity",
      "slots":
      [
          {
            "name": "City",
            "type": "AMAZON.US_CITY"
          }
      ]
    }, 

CustomerName {CustName}
CustomerCity {City}


    Output speech = "Please tell your name"
----------------------------------------------------------
     {
      "intent": "Customerdetails",
      "slots":
      [
        {
          "name": "CustName",
          "type": "AMAZON.US_FIRST_NAME"
        },
        {
          "name": "City",
          "type": "AMAZON.US_CITY"
        }
      ]
    },



Customerdetails {CustName} and {City}
Customerdetails {CustName} {City}
Customerdetails {City} and {CustName}
Customerdetails {City} {CustName}
Customerdetails {CustName} and {City}
Customerdetails {CustName} {City}
Customerdetails {CustName}
Customerdetails {City}

  

    {
      "intent": "CustomerName",
      "slots":
      [
          {
            "name": "CustName",
            "type": "AMAZON.US_FIRST_NAME"
          }
      ]
    },  
    {
      "intent": "Customerdetails",
      "slots":
      [
        {
          "name": "CustStreet",
          "type": "AMAZON.StreetAddress"
        },
        {
          "name": "CustAddress",
          "type": "AMAZON.PostalAddress"
        },
        {
          "name": "City",
          "type": "AMAZON.US_CITY"
        }
      ]
    },
      

CustomerName {CustName}
CustomerName {CustName} {CustName}

Customerdetails {CustStreet} {CustAddress} {City}
Customerdetails Address {CustStreet} {CustAddress} City {City}
Customerdetails from {City}
Customerdetails Address {CustStreet} {CustAddress} City {City}
Customerdetails from {CustStreet} {CustName} 
Customerdetails {CustStreet} {CustAddress} {City}
Customerdetails {CustStreet} {CustAddress}
Customerdetails {CustAddress} {City}
Customerdetails {CustStreet} {City}
Customerdetails {CustAddress} {CustStreet} {City}
Customerdetails {City}