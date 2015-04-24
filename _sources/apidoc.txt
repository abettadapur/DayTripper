
REST API Documentation
=================================

The Day Tripper REST API can be used to interface with the application and its recommendations engine. All requests except those in the auth section require the token query parameter, which is a Facebook OAUTH token that has been previously verified with the DayTripper service. This token is used to both authenticate the user and provide user identity information.

Authentication
-------------------------------

.. http:post:: /auth/verify

  Registers a Facebook authentication token with the server. The Facebook token must be a valid token that matches the Facebook user-id provided. This must be called once before using the API with a Facebook token. If the user-id and the token do not match, a 401 HTTP response will be returned.

  **Request**

  .. code-block:: js

    POST /auth/verify
    Content-Type: application/json

    {
      "token": ".....",
      "user_id": "...."
    }

.. http:delete:: /auth/logout

  Logout and delete the Facebook token from the database. The token will no longer be valid and any requests made with it will be rejected. A call to /auth/verify is required to continue using the API.

  :query token: The token to logout.

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

.. http:post:: /itinerary/<int:id>/copy

  Copy another user's public itinerary and all of the associated items to the current account. The POST body can optionally contain a date to assign to the copied itinerary.

  **Request**

  .. code-block:: js

    POST /itinerary/1/copy
    Content-Type: application/json

    {
      "date": "2015-03-31T00:00:00-0400"
    }

  **Response**

  .. sourcecode:: js

    HTTP/1.1 200 OK
    Content-Type: application/json

    {
      "city":"Atlanta",
      "date":"2015-03-31T00:00:00-0400",
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

The ratings resource allows users to rate other users itineraries. A simple star rating method is used.

.. http:post:: /itinerary/<int:id>/rating/create

  Creates a rating for the specified itinerary

  **Request**

  .. code-block:: js

    POST /itinerary/1/ratings/create
    Content-Type: application/json

    {
      "rating": 5
    }

  **Response**

  .. code-block:: js

    HTTP/1.1 201 Created

    {
      "rating": 5
    }

.. http:get:: /itinerary/1/ratings/1

  Gets a specific rating for the specified itinerary

  **Response**

  .. code-block:: js

    HTTP/1.1 201 Created

    {
      "rating": 5
    }

.. http:get:: /itinerary/1/ratings/list

.. http:put:: /itinerary/1/ratings/1



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
      "category": "breakfast",
      "end_time": "2015-04-05T08:45:47-04:00",
      "name": "Ria's Bluebird",
      "start_time": "2015-04-05T08:00:47-04:00",
      "yelp_id": "rias-bluebird-atlanta"
    }

  **Response**

  .. code-block:: js

    HTTP/1.1 201 Created

    {
      "category": "breakfast",
      "end_time": "2015-04-05T08:45:47-04:00",
      "id": 1,
      "name": "Ria's Bluebird",
      "start_time": "2015-04-05T08:00:47-04:00",
      "yelp_entry": {
        "id": "rias-bluebird-atlanta",
        "image_url": "http://s3-media2.fl.yelpassets.com/bphoto/ICjCwjkEcmzMEdLbLGXHMQ/ms.jpg",
        "location":{
          "address": "421 Memorial Dr SE",
          "city": "Atlanta",
          "coordinate":{"latitude": 33.746578, "longitude": -84.373642},
          "postal_code": 30312,
          "state_code": "GA",
          "yelp_id": "rias-bluebird-atlanta"
        },
        "name": "Ria's Bluebird",
        "phone": "4045213737",
        "price": 2,
        "rating": 4,
        "review_count": 570,
        "url": "http://www.yelp.com/biz/rias-bluebird-atlanta"
      }
      "yelp_id": "rias-bluebird-atlanta"
    }

.. http:get:: /itinerary/<int:id>/item/<int:id>

  Gets the specified item.

  **Response**

  .. code-block:: js

    HTTP/1.1 201 Created

    {
      "category": "breakfast",
      "end_time": "2015-04-05T08:45:47-04:00",
      "id": 1,
      "name": "Ria's Bluebird",
      "start_time": "2015-04-05T08:00:47-04:00",
      "yelp_entry": {
        "id": "rias-bluebird-atlanta",
        "image_url": "http://s3-media2.fl.yelpassets.com/bphoto/ICjCwjkEcmzMEdLbLGXHMQ/ms.jpg",
        "location":{
          "address": "421 Memorial Dr SE",
          "city": "Atlanta",
          "coordinate":{"latitude": 33.746578, "longitude": -84.373642},
          "postal_code": 30312,
          "state_code": "GA",
          "yelp_id": "rias-bluebird-atlanta"
        },
        "name": "Ria's Bluebird",
        "phone": "4045213737",
        "price": 2,
        "rating": 4,
        "review_count": 570,
        "url": "http://www.yelp.com/biz/rias-bluebird-atlanta"
      }
      "yelp_id": "rias-bluebird-atlanta"
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
      "category": "breakfast",
      "end_time": "2015-04-05T08:45:47-04:00",
      "id": 1,
      "name": "Ria's Bluebird",
      "start_time": "2015-04-05T08:00:47-04:00",
      "yelp_entry": {
        "id": "rias-bluebird-atlanta",
        "image_url": "http://s3-media2.fl.yelpassets.com/bphoto/ICjCwjkEcmzMEdLbLGXHMQ/ms.jpg",
        "location":{
          "address": "421 Memorial Dr SE",
          "city": "Atlanta",
          "coordinate":{"latitude": 33.746578, "longitude": -84.373642},
          "postal_code": 30312,
          "state_code": "GA",
          "yelp_id": "rias-bluebird-atlanta"
        },
        "name": "Ria's Bluebird",
        "phone": "4045213737",
        "price": 2,
        "rating": 4,
        "review_count": 570,
        "url": "http://www.yelp.com/biz/rias-bluebird-atlanta"
      }
      "yelp_id": "rias-bluebird-atlanta"
    }

.. http:delete:: /itinerary/<int:id>/item/<int:id>

  Deletes the specified item

  **Response**

  .. code-block:: js

    HTTP/1.1 204 No Content

    true

.. http:get:: /itinerary/<int:id>/item/<int:id>/query

  Returns a different suggested YelpEntry for this item.

  **Request**

  .. code-block:: js

    GET itinerary/6/item/22/query?token=token&strategy=yelp-rating&dids=gusto-wood-fire-grill-atlanta&dids=ocean-market-downtown-atlanta

  **Response**

  .. code-block:: js

    HTTP/1.1 200 OK

    {
        "id": "get-fruity-cafe-atlanta-2",
        "image_url": "http://s3-media4.fl.yelpassets.com/bphoto/4aCT0WPU_cI9dpM4Ia_k_g/ms.jpg",
        "location": {
            "address": "79 Marietta St NW",
            "city": "Atlanta",
            "coordinate": {
                "latitude": 33.7564522,
                "longitude": -84.391679
            },
            "postal_code": 30303,
            "state_code": "GA",
            "yelp_id": "get-fruity-cafe-atlanta-2"
        },
        "name": "Get Fruity Cafe",
        "phone": "4045210109",
        "price": 1,
        "rating": 4.5,
        "review_count": 64,
        "url": "http://www.yelp.com/biz/get-fruity-cafe-atlanta-2"
    }

  :query strategy:  one of [distance, yelp-rating, price-0, price-1, price-2, price-3, price-4, random, popularity, first] (defaults to random)
  :query dids: additional YelpIDs that server is not allowed to return


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
		//google directions content
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
  
Experimental
----------------------------------
.. http:post:: /experiment/itinerary/create
  
  Creates an itinerary using an improved item selection algorithm. The parameters are the same as the regular itinerary create endpoint.
  
  **Request**

    .. code-block:: js

      POST /experiment/itinerary/create
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
