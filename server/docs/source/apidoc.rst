
REST API Documentation
=================================

The DayTripper REST API can be used to interface with the application and its recommendations engine. All requests except those in the auth section require the token query parameter, which is a Facebook OAUTH token that has been previously verified with the DayTripper service. This token is used to both authenticate the user and provide user identity information.

Authentication
-------------------------------

Itineraries
----------------

The itineraries resource represents all itineraries that are currently present in the application.

.. http:post:: /itinerary/create

    Creates an itinerary with the specified parameters. The itinerary will be prefilled with items based on the time and location specified.

    **Request**

    .. code-block:: js

      POST /itinerary/create
      Content-Type: application/json

       {
           "city":"Atlanta",
           "date":"2015-03-31T01:30:53-0400",
           "end_time":"2015-03-31T21:00:53-0400",
           "name":"Sample Itinerary",
           "start_time":"2015-03-31T10:00:53-0400"
        }

    **Response**

    .. sourcecode:: js

      HTTP/1.1 201 Created
      Content-Type: application/json

      {
        "city":"Atlanta",
        "date":"2015-03-31T01:30:53-0400",
        "end_time":"2015-03-31T21:00:53-0400",
        "id":14,
        "items":[...]
        "name":"Sample Itinerary",
        "start_time":"2015-03-31T10:00:53-0400",
        "user":{...}
      }


.. http:get:: /itinerary/<int:id>

    Retrieve an itinerary with the id specified from the database. Comes with the associated items and user. Users can only retrieve itineraries that are theirs.

    **Response**

    .. sourcecode:: js

        HTTP/1.1 201 OK
        ContentType: application/json

        {
           "city":"Atlanta",
           "date":"2015-03-31T01:30:53-0400",
           "end_time":"2015-03-31T21:00:53-0400",
           "id":14,
           "items":[
               {
                 "category":"lunch",
                 "end_time":"2015-03-31T11:30:53-04:00",
                 "id":32,
                 "name":"Heirloom Market BBQ",
                 "start_time":"2015-03-31T10:00:53-04:00",
                 "yelp_entry":{
                    "id":"heirloom-market-bbq-atlanta",
                    "image_url":"http://s3-media1.fl.yelpassets.com/bphoto/nxPlyqHrLCNMnDe87P0yLQ/ms.jpg",
                    "location":{
                       "address":"2243 Akers Mill Rd SE",
                       "city":"Atlanta",
                       "coordinate":{
                          "latitude":33.8986473470416,
                          "longitude":-84.4471785276031
                       },
                       "postal_code":30339,
                       "state_code":"GA",
                       "yelp_id":"heirloom-market-bbq-atlanta"
                    },
                    "name":"Heirloom Market BBQ",
                    "phone":"7706122502",
                    "price":2,
                    "rating":4.5,
                    "review_count":688,
                    "url":"http://www.yelp.com/biz/heirloom-market-bbq-atlanta"
                 },
                "yelp_id":"heirloom-market-bbq-atlanta"
           ]
           "name":"Sample Itinerary",
           "start_time":"2015-03-31T10:00:53-0400",
           "user":{
                "email":"alexbettadapur@gmail.com",
                "first_name":"Alex",
                "id":10206134897237072,
                "last_name":"Bettadapur"
            }
        }

.. http:get:: /itinerary/list
  
  Gets all the itineraries that the user owns.

  **Response**

  .. sourcecode:: js

      HTTP/1.1 201 OK
      ContentType: application/json

      [
        {
           "city":"Atlanta",
           "date":"2015-03-31T01:30:53-0400",
           "end_time":"2015-03-31T21:00:53-0400",
           "id":14,
           "items":[
               {
                 "category":"lunch",
                 "end_time":"2015-03-31T11:30:53-04:00",
                 "id":32,
                 "name":"Heirloom Market BBQ",
                 "start_time":"2015-03-31T10:00:53-04:00",
                 "yelp_entry":{
                    "id":"heirloom-market-bbq-atlanta",
                    "image_url":"http://s3-media1.fl.yelpassets.com/bphoto/nxPlyqHrLCNMnDe87P0yLQ/ms.jpg",
                    "location":{
                       "address":"2243 Akers Mill Rd SE",
                       "city":"Atlanta",
                       "coordinate":{
                          "latitude":33.8986473470416,
                          "longitude":-84.4471785276031
                       },
                       "postal_code":30339,
                       "state_code":"GA",
                       "yelp_id":"heirloom-market-bbq-atlanta"
                    },
                    "name":"Heirloom Market BBQ",
                    "phone":"7706122502",
                    "price":2,
                    "rating":4.5,
                    "review_count":688,
                    "url":"http://www.yelp.com/biz/heirloom-market-bbq-atlanta"
                 },
                "yelp_id":"heirloom-market-bbq-atlanta"
           ]
           "name":"Sample Itinerary",
           "start_time":"2015-03-31T10:00:53-0400",
           "user":{
                "email":"alexbettadapur@gmail.com",
                "first_name":"Alex",
                "id":10206134897237072,
                "last_name":"Bettadapur"
            }
        },
        ...
      ]


.. http:put:: /itinerary/<int:id>
  
  Update an exisiting itinerary with new information. This should only be used to update itinerary attributes, not add or remove items. Users can only edit itineraries that are theirs.

  **Request**

  .. code-block:: js

    PUT /itinerary/create
    Content-Type: application/json

      {
         "city":"Atlanta",
         "date":"2015-03-31T01:30:53-0400",
         "end_time":"2015-03-31T21:00:53-0400",
         "name":"Sample Itinerary",
         "start_time":"2015-03-31T10:00:53-0400"
      } 

  **Response**

  .. sourcecode:: js

    HTTP/1.1 200 OK
    Content-Type: application/json

    {
      "city":"Atlanta",
      "date":"2015-03-31T01:30:53-0400",
      "end_time":"2015-03-31T21:00:53-0400",
      "id":14,
      "items":[...]
      "name":"Sample Itinerary",
      "start_time":"2015-03-31T10:00:53-0400",
      "user":{...}
    }


.. http:delete:: /itinerary/<int:id>

  Delete the itinerary with the specified Id. Users can only delete itineraries that are theirs

  **Response**

  .. sourcecode:: js

    HTTP/1.1 204 No Content
  
    true


Search Itineraries 
----------------------

Users can also search for itineraries from other users using the search endpoint.

.. http:get:: /itinerary/search
  
  Search for an itinerary

  **Response**

  .. sourcecode:: js

      HTTP/1.1 201 OK
      ContentType: application/json

      [
        {
           "city":"Atlanta",
           "date":"2015-03-31T01:30:53-0400",
           "end_time":"2015-03-31T21:00:53-0400",
           "id":14,
           "items":[
               {
                 "category":"lunch",
                 "end_time":"2015-03-31T11:30:53-04:00",
                 "id":32,
                 "name":"Heirloom Market BBQ",
                 "start_time":"2015-03-31T10:00:53-04:00",
                 "yelp_entry":{
                    "id":"heirloom-market-bbq-atlanta",
                    "image_url":"http://s3-media1.fl.yelpassets.com/bphoto/nxPlyqHrLCNMnDe87P0yLQ/ms.jpg",
                    "location":{
                       "address":"2243 Akers Mill Rd SE",
                       "city":"Atlanta",
                       "coordinate":{
                          "latitude":33.8986473470416,
                          "longitude":-84.4471785276031
                       },
                       "postal_code":30339,
                       "state_code":"GA",
                       "yelp_id":"heirloom-market-bbq-atlanta"
                    },
                    "name":"Heirloom Market BBQ",
                    "phone":"7706122502",
                    "price":2,
                    "rating":4.5,
                    "review_count":688,
                    "url":"http://www.yelp.com/biz/heirloom-market-bbq-atlanta"
                 },
                "yelp_id":"heirloom-market-bbq-atlanta"
           ]
           "name":"Sample Itinerary",
           "start_time":"2015-03-31T10:00:53-0400",
           "user":{
                "email":"alexbettadapur@gmail.com",
                "first_name":"Alex",
                "id":10206134897237072,
                "last_name":"Bettadapur"
            }
        },
        ...
      ]

  :query query: The search term -- required
  :query city: An optional city to filter by


Itinerary Ratings
--------------------------------------


Items
------------------------------------

The items resource represents the individual events contained within an itinerary. This resource can be used to manually add, update, or delete items from a pre-existing itinerary. It can also be used to get detailed information about a specific event.

.. http:post:: /itinerary/<int:id>/item/create

  Creates an item with the specified parameters and adds it to the specified itinerary

  **Request**

  .. code-block:: js

    POST /itinerary/1/items/create
    Content-Type: application/json

    {
    }

  **Response**

  .. code-block:: js

    HTTP/1.1 201 Created

    {
    }

.. http:get:: /itinerary/<int:id>/item/<int:id>

  Gets the specified item.

  **Response**

  .. code-block:: js

    HTTP/1.1 201 Created

    {
    }

.. http:put:: /itinerary/<int:id>/item/<int:id>

  Updates an item with new details as specified.

  **Request**

  .. code-block:: js

    PUT /itinerary/1/items/1
    Content-Type: application/json

    {
    }

  **Response**

  .. code-block:: js

    HTTP/1.1 200 OK

    {
    }

.. http:delete:: /itinerary/<int:id>/item/<int:id>
  
  Deletes the specified item

  **Response**

  .. code-block:: js

    HTTP/1.1 204 No Content

    true


Categories
-----------------------------------


Directions
-----------------------------------------------

.. http:get:: /maps/directions

  Gets directions from the Google Directions API. 

  **Response**

  .. code-block:: js

    HTTP/1.1 200 OK

    {

    }

  :query origin: The start location. This can be an address string or coordinates. --- required
  :query destination: The end location. This can be an address string or coordinates. --- required


.. http:get:: /maps/polyline

  Gets a Google Encoded polyline for use on a map. See here for more information

  **Response**

  .. code-block:: js

    HTTP/1.1 200 OK

    fldkjadsfias;odfjsa;ijkfdas

  :query origin: The start location. This can be an address string or coordinates. --- required
  :query destination: The end location. This can be an address string or coordinates. --- required











