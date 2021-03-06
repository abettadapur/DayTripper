from flask import Flask
from flask_restful import Api

import api as restapi

app = Flask(__name__)
app.debug=True
api = Api(app)

#Add the resources from the API file to routes

api.add_resource(restapi.Test, '/test')
api.add_resource(restapi.Test2, '/test/<string:parameter>')

api.add_resource(restapi.AuthResource, '/auth/verify')
api.add_resource(restapi.AuthLogoutResource, '/auth/logout')

api.add_resource(restapi.ExperimentCreateItineraryResource, '/experiment/itinerary/create')

api.add_resource(restapi.CreateItineraryResource, '/itinerary/create')
api.add_resource(restapi.ItineraryResource, '/itinerary/<int:id>')
api.add_resource(restapi.ListItineraryResource, '/itinerary/list')
api.add_resource(restapi.SearchItineraryResource, '/itinerary/search')
api.add_resource(restapi.RandomizeItineraryResource, '/itinerary/<int:id>/randomize')
api.add_resource(restapi.CopyItineraryResource, '/itinerary/<int:id>/copy')

api.add_resource(restapi.ItemResource, '/itinerary/<int:itinerary_id>/item/<int:id>')
api.add_resource(restapi.CreateItemResource, '/itinerary/<int:itinerary_id>/item/create')

api.add_resource(restapi.FetchYelpResource, '/itinerary/<int:itinerary_id>/item/<int:item_id>/query')

api.add_resource(restapi.CreateRatingResource, '/itinerary/<int:itinerary_id>/rating/create')
api.add_resource(restapi.RatingResource, '/itinerary/<int:itinerary_id>/rating/<int:id>')
api.add_resource(restapi.ListRatingResource, '/itinerary/<int:itinerary_id>/rating/list')

api.add_resource(restapi.ListCategoryResource, '/category/list')
api.add_resource(restapi.QueryCategoryResource, '/category/<string:category_str>/query')

api.add_resource(restapi.DirectionsResource, '/maps/directions')
api.add_resource(restapi.PolylineResource, '/maps/polyline')




#Run the server on port 5000
if __name__ == '__main__':
	#http_server = WSGIServer(('0.0.0.0', 3000), app)

	#http_server.serve_forever()

	#debug server. Uncomment above for production
	#import localtest
	#localtest.init_db()
	app.run(host='0.0.0.0', port=3000)
