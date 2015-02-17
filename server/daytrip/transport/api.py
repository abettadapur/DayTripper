from flask import request
from flask_restful import Resource, reqparse

class Test(Resource):
	def get(self):
		return {"message": "HelloWorld"}, 200  #Return a python object and a status code!


class Test2(Resource):
	def post(self, parameter):
		json_data = request.get_json(force=True)
		return {"received": json_data, "parameter": parameter}, 200 #Return the posted data with a status code