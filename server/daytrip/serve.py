from etc import config
from flask import Flask
from flask_restful import Api

from transport import api as restapi
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
api = Api(app)

#Add the resources from the API file to routes

api.add_resource(restapi.Test, '/test')
api.add_resource(restapi.Test2, '/test/<string:parameter>')


#Run the server on port 5000
if __name__ == '__main__':
	http_server = WSGIServer(('0.0.0.0', 5000), app)

	http_server.serve_forever()
