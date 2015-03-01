from etc import config
from flask import Flask
from flask_restful import Api

from transport import api as restapi
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
app.debug=True
api = Api(app)

#Add the resources from the API file to routes

api.add_resource(restapi.Test, '/test')
api.add_resource(restapi.Test2, '/test/<string:parameter>')
api.add_resource(restapi.Auth, '/auth/verify')
api.add_resource(restapi.Create_Itinerary, '/itinerary/create')
api.add_resource(restapi.Itinerary, '/itinerary/<int:id>')

#Will be changed
api.add_resource(restapi.Item, '/itinerary/<int:itinerary_id>/item/<int:id>')


#Run the server on port 5000
if __name__ == '__main__':
	#http_server = WSGIServer(('0.0.0.0', 3000), app)

	#http_server.serve_forever()

	#debug server. Uncomment above for production
	app.run(host='0.0.0.0', port=3000)
