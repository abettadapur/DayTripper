import facebook
from flask import request
from flask_restful import Resource, reqparse
import db

class Test(Resource):
	def get(self):
		return {"message": "HelloWorld"}, 200  #Return a python object and a status code!


class Test2(Resource):
	def post(self, parameter):
		json_data = request.get_json(force=True)
		return {"received": json_data, "parameter": parameter}, 200 #Return the posted data with a status code


class Auth(Resource):

	def post(self):
		json_data = request.get_json(force=True)
		token = json_data['token']
		uid = json_data['user_id']

		graph = facebook.GraphAPI(access_token=token)
		user = graph.get_object(id=uid)
		if(user and user['id']==uid):

			#add token to repository if not exists
			if not db.sqlite.check_authorization(token):
				db.sqlite.add_authorization(token, uid)

			#add to user repository if not exists
			if not db.sqlite.user_exists(uid):
				db.sqlite.create_user(uid, user['first_name'], user['last_name'], user['email'])

			return True, 200;
