import facebook
from flask import request
from flask_restful import Resource, reqparse, abort
import db
import model
import datetime
import dateutil.parser
from model.itinerary import Itinerary
from model.itinerary_rating import ItineraryRating
from model.item import Item
from model.user import User
from maps import maps
import random

from yelp import yelpapi



#ALL QUERIES MUST BE AUTHENTICATED WITH AN AUTHENTICATION TOKEN (Except for the AUTH POST)

#Add the token as part of a query string, and check db.sqlite.check_authorization(token)

UNAUTHORIZED_RESPONSE = ('Do not own resource', 401)


class Test(Resource):
    def get(self):
        db.sqlite.get_itinerary(1)
        return {"message": "HelloWorld"}, 200  #Return a python object and a status code!


class Test2(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('items', type=list, required=True, help='no items', location='json')

    def post(self, parameter):
        #json_data = request.get_json(force=True)
        #return {"received": json_data, "parameter": parameter}, 200 #Return the posted data with a status code
        args = self.reqparse.parse_args()
        items = args['items']
        print items
        return items[0]['id'], 200


class AuthResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('token', type=str, required = True, help="No token to verify", location='json')
        self.reqparse.add_argument('user_id', type=str, required = True, help="An associated Facebook User ID is required", location='json')
        super(AuthResource, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        token = args['token']
        uid = args['user_id']

        graph = facebook.GraphAPI(access_token=token)
        user = graph.get_object(id=uid)
        if(user and user['id']==uid):

            #add token to repository if not exists
            if not db.sqlite.check_authorization(token):
                db.sqlite.insert_authorization(token, uid)

            #add to user repository if not exists
            if not db.sqlite.user_exists(uid):
                new_user = User(uid, user['first_name'], user['last_name'], user['email'])
                db.sqlite.insert_user(new_user)

            return True, 200


class ItineraryResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('token', type=str, required=True, location='args', help='No token to verify')

        self.put_reqparse = self.reqparse.copy()
        self.put_reqparse.add_argument('name', type=str, required=True, location='json', help='No name provided')
        self.put_reqparse.add_argument('date', type=str, required=True, location='json', help='No date provided')
        self.put_reqparse.add_argument('start_time', type=str, required=True, location='json', help='No start_time provided')
        self.put_reqparse.add_argument('end_time', type=str, required=True, location='json', help='No end_time provided')
        self.put_reqparse.add_argument('city', type=str, required=True, location='json', help='No city provided')
        self.put_reqparse.add_argument('items', type=list, required=True, location='json', help='No items field provided')

        super(ItineraryResource, self).__init__()

    def get(self, id):
        args = self.reqparse.parse_args()
        user_id = get_uid_or_abort_on_bad_token(args['token'])
        itinerary = db.sqlite.get_itinerary(id)
        abort_on_invalid_itinerary(itinerary, user_id)
        return itinerary.as_dict()

    def put(self, id):
        args = self.put_reqparse.parse_args()
        user_id = get_uid_or_abort_on_bad_token(args['token'])

        old_itinerary = db.sqlite.get_itinerary(id)

        abort_on_invalid_itinerary(old_itinerary, user_id)

        # TODO give creation ability through put?
        updated_itinerary = Itinerary(
            id=id,
            user=db.sqlite.get_user(user_id),
            name=args['name'],
            date=args['date'],
            start_time=args['start_time'],
            end_time=args['end_time'],
            city=args['city'],
            items=old_itinerary.items
        )
        db.sqlite.update_itinerary(updated_itinerary)
        return db.sqlite.get_itinerary(id).as_dict()

    def delete(self, id):
        args = self.reqparse.parse_args()
        user_id = get_uid_or_abort_on_bad_token(args['token'])

        itinerary = db.sqlite.get_itinerary(id)

        # add before "abort_on..." because null itinerary is valid for DELETE
        if not itinerary:
            return True, 204
        abort_on_invalid_itinerary(itinerary, user_id)

        db.sqlite.delete_itinerary(id)
        return True, 204


class CreateItineraryResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('token', type=str, required=True, location='args', help='No token to verify')
        self.reqparse.add_argument('name', type=str, required=True, location='json', help='No name provided')
        self.reqparse.add_argument('date', type=str, required=True, location='json', help='No date provided')
        self.reqparse.add_argument('start_time', type=str, required=True, location='json', help='No start_time provided')
        self.reqparse.add_argument('end_time', type=str, required=True, location='json', help='No end_time provided')
        self.reqparse.add_argument('city', type=str, required=True, location='json', help='No city provided')

        super(CreateItineraryResource, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        user_id = get_uid_or_abort_on_bad_token(args['token'])
        start_time = dateutil.parser.parse(args['start_time'])
        end_time = dateutil.parser.parse(args['end_time'])
        date = dateutil.parser.parse(args['date'])

        if (end_time - start_time).seconds // 3600 < 6:
            pass  #ABORT

        itinerary = Itinerary(
            id=None,
            user=db.sqlite.get_user(user_id),
            name=args['name'],
            date=args['date'],
            start_time=args['start_time'],
            end_time=args['end_time'],
            city=args['city'],
            items=[]
        )
        itinerary_id = db.sqlite.insert_itinerary(itinerary)
        itinerary = db.sqlite.get_itinerary(itinerary_id)



        #Add some sample items based on times
        # TODO(abettadapur): ITEM TIMES MUST BE FIXED TO ALLOW FOR TRANSPORT
        # TODO(abettadapur): THIS ROUTINE SHOULD BE METHODIZED
        # TODO(abettadapur): THIS TAKES 20 SECONDS, MAYBE BETTER FASTER, CACHE SAMPLE ITINERARIES?

        if start_time <= date.replace(hour=10, minute=0, second=0, microsecond=0):
            category = model.match_category('breakfast')
            results = yelpapi.search("", itinerary.city, category.filters)
            random_index = random.randint(0,15)
            item = Item(
                id = None,
                yelp_id = results[random_index]['id'],
                category = 'breakfast',
                name = results[random_index]['name'],
                start_time = start_time.isoformat(),
                end_time = (start_time + datetime.timedelta(hours=1, minutes=30)).isoformat(),
            )
            db.sqlite.insert_item(item, itinerary)
            itinerary = db.sqlite.get_itinerary(itinerary_id)

        if end_time >= date.replace(hour=11, minute=0, second=0, microsecond=0):
            category = model.match_category('lunch')
            results = yelpapi.search(category.search_term, itinerary.city, category.filters)

            random_index = random.randint(0,15)
            if len(itinerary.items) == 0:
                item = Item(
                    id = None,
                    yelp_id = results[random_index]['id'],
                    category = 'lunch',
                    name = results[random_index]['name'],
                    start_time = start_time.isoformat(),
                    end_time = (start_time + datetime.timedelta(hours=1, minutes=30)).isoformat(),
                )
                db.sqlite.insert_item(item, itinerary)
                itinerary = db.sqlite.get_itinerary(itinerary_id)
            else:
                origin = [itinerary.items[len(itinerary.items)-1].yelp_entry.location.address]
                destinations = [r['location']['address'][0] for r in results]
                index = maps.closest_item(origin, destinations)
                item = Item(
                    id = None,
                    yelp_id = results[index]['id'],
                    category = 'lunch',
                    name = results[index]['name'],
                    start_time = start_time.isoformat(),
                    end_time = (start_time + datetime.timedelta(hours=1, minutes=30)).isoformat(),
                )
                db.sqlite.insert_item(item, itinerary)
                itinerary = db.sqlite.get_itinerary(itinerary_id)

        if end_time >= date.replace(hour=14, minute=0, second=0, microsecond=0):
            category = model.match_category('attraction')
            results = yelpapi.search(category.search_term, itinerary.city, category.filters)

            random_index = random.randint(0,15)
            if len(itinerary.items) == 0:
                item = Item(
                    id = None,
                    yelp_id = results[random_index]['id'],
                    category = 'attraction',
                    name = results[random_index]['name'],
                    start_time = start_time.isoformat(),
                    end_time = (start_time + datetime.timedelta(hours=1, minutes=30)).isoformat(),
                )
                db.sqlite.insert_item(item, itinerary)
                itinerary = db.sqlite.get_itinerary(itinerary_id)
            else:
                origin = [itinerary.items[len(itinerary.items)-1].yelp_entry.location.address]
                destinations = [r['location']['address'][0] for r in results]
                index = maps.closest_item(origin, destinations)
                item = Item(
                    id = None,
                    yelp_id = results[index]['id'],
                    category = 'attraction',
                    name = results[index]['name'],
                    start_time = start_time.isoformat(),
                    end_time = (start_time + datetime.timedelta(hours=1, minutes=30)).isoformat(),
                )
                db.sqlite.insert_item(item, itinerary)
                itinerary = db.sqlite.get_itinerary(itinerary_id)

        if end_time >= date.replace(hour=18, minute=0, second=0, microsecond=0):
            category = model.match_category('dinner')
            results = yelpapi.search(category.search_term, itinerary.city, category.filters)
            random_index = random.randint(0,15)
            if len(itinerary.items) == 0:
                item = Item(
                    id = None,
                    yelp_id = results[random_index]['id'],
                    category = 'dinner',
                    name = results[random_index]['name'],
                    start_time = start_time.isoformat(),
                    end_time = (start_time + datetime.timedelta(hours=1, minutes=30)).isoformat(),
                )
                db.sqlite.insert_item(item, itinerary)
                itinerary = db.sqlite.get_itinerary(itinerary_id)
            else:
                origin = [itinerary.items[len(itinerary.items)-1].yelp_entry.location.address]
                destinations = [r['location']['address'][0] for r in results]
                index = maps.closest_item(origin, destinations)
                item = Item(
                    id = None,
                    yelp_id = results[index]['id'],
                    category = 'dinner',
                    name = results[index]['name'],
                    start_time = start_time.isoformat(),
                    end_time = (start_time + datetime.timedelta(hours=1, minutes=30)).isoformat(),
                )
                db.sqlite.insert_item(item, itinerary)
                itinerary = db.sqlite.get_itinerary(itinerary_id)

        if end_time >= date.replace(hour=21, minute=0, second=0, microsecond=0):
            category = model.match_category('nightlife')
            results = yelpapi.search(category.search_term, itinerary.city, category.filters)
            random_index = random.randint(0,15)
            if len(itinerary.items) == 0:
                item = Item(
                    id = None,
                    yelp_id = results[random_index]['id'],
                    category = 'nightlife',
                    name = results[random_index]['name'],
                    start_time = start_time.isoformat(),
                    end_time = (start_time + datetime.timedelta(hours=1, minutes=30)).isoformat(),
                )
                db.sqlite.insert_item(item, itinerary)
                itinerary = db.sqlite.get_itinerary(itinerary_id)
            else:
                origin = [itinerary.items[len(itinerary.items)-1].yelp_entry.location.address]
                destinations = [r['location']['address'][0] for r in results]
                index = maps.closest_item(origin, destinations)
                item = Item(
                    id = None,
                    yelp_id = results[index]['id'],
                    category = 'nightlife',
                    name = results[index]['name'],
                    start_time = start_time.isoformat(),
                    end_time = (start_time + datetime.timedelta(hours=1, minutes=30)).isoformat(),
                )
                db.sqlite.insert_item(item, itinerary)
                itinerary = db.sqlite.get_itinerary(itinerary_id)

        return itinerary.as_dict(), 201


class ListItineraryResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("token", type=str, required=True, location='args', help='Missing auth token')


    def get(self):
        args = self.reqparse.parse_args()

        user_id = get_uid_or_abort_on_bad_token(args['token'])
        itineraries = db.sqlite.list_itineraries(user_id)
        itineraries_dict = [i.as_dict() for i in itineraries]
        return itineraries_dict


class ItemResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('token', type=str, required=True, location='args', help='No token to verify')

        self.put_reqparse = self.reqparse.copy()
        self.put_reqparse.add_argument('yelp_id', type=str, required=True, location='json', help='Missing yelp_id')
        self.put_reqparse.add_argument('category', type=str, required=True, location='json', help='Missing category')
        self.put_reqparse.add_argument('name', type=str, required=True, location='json', help='Missing name')
        self.put_reqparse.add_argument('start_time', type=str, required=True, location='json', help='Missing start_time')
        self.put_reqparse.add_argument('end_time', type=str, required=True, location='json', help='Missing end_time')
        super(ItemResource, self).__init__()

    def get(self, itinerary_id, id):
        args = self.reqparse.parse_args()

        user_id = get_uid_or_abort_on_bad_token(args['token'])
        item = db.sqlite.get_item(id)

        abort_on_invalid_item_relation(item, itinerary_id, user_id)
        return item.as_dict()

    def put(self, itinerary_id, id):
        args = self.put_reqparse.parse_args()

        user_id = get_uid_or_abort_on_bad_token(args['token'])
        old_item = db.sqlite.get_item(id)

        abort_on_invalid_item_relation(old_item, itinerary_id, user_id)

        updated_item = Item(
            id=id,
            yelp_id=args['yelp_id'],
            category=args['category'],
            name=args['name'],
            start_time=args['start_time'],
            end_time=args['end_time']
        )
        db.sqlite.update_item(updated_item, itinerary_id)
        return db.sqlite.get_item(id).as_dict()

    def delete(self, itinerary_id, id):
        args = self.reqparse.parse_args()

        user_id = get_uid_or_abort_on_bad_token(args['token'])
        item = db.sqlite.get_item(id)

        # add before "abort_on..." because null itinerary is valid for DELETE
        if not item:
            return True, 204
        abort_on_invalid_item_relation(item, itinerary_id, user_id)

        db.sqlite.delete_item(id)
        return True, 204


class CreateItemResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('token', type=str, required=True, location='args', help='No token to verify')
        self.reqparse.add_argument('yelp_id', type=str, required=True, location='json', help='Missing yelp_id')
        self.reqparse.add_argument('category', type=str, required=True, location='json', help='Missing category')
        self.reqparse.add_argument('name', type=str, required=True, location='json', help='Missing name')
        self.reqparse.add_argument('start_time', type=str, required=True, location='json', help='Missing start_time')
        self.reqparse.add_argument('end_time', type=str, required=True, location='json', help='Missing end_time')
        super(CreateItemResource, self).__init__()

    def post(self, itinerary_id):
        args = self.reqparse.parse_args()

        user_id = get_uid_or_abort_on_bad_token(args['token'])
        itinerary = db.sqlite.get_itinerary(itinerary_id)

        abort_on_invalid_itinerary(itinerary, user_id)

        item = Item(
            id=None,
            yelp_id=args['yelp_id'],
            category=args['category'],
            name=args['name'],
            start_time=args['start_time'],
            end_time=args['end_time']
        )
        item_id = db.sqlite.insert_item(item, itinerary)
        return db.sqlite.get_item(item_id).as_dict(), 201


class CreateRatingResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('token', type=str, required=True, location='args', help='No token to verify')
        self.reqparse.add_argument('rating', type=int, required=True, location='json', help='No rating given')
        super(CreateRatingResource, self).__init__()

    def post(self, itinerary_id):
        args = self.reqparse.parse_args()

        user_id = get_uid_or_abort_on_bad_token(args['token'])
        rating_id = db.sqlite.insert_itinerary_rating(itinerary_id, user_id, args['rating'])
        return db.sqlite.get_itinerary_rating(rating_id).as_dict(), 201


class RatingResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('token', type=str, required=True, location='args', help='No token to verify')

        self.put_reqparse = self.reqparse.copy()
        self.put_reqparse.add_argument('rating', type=int, required=True, location='json', help='No rating given')

        super(RatingResource, self).__init__()

    def get(self, itinerary_id, id):
        print "HELLO"
        args = self.reqparse.parse_args()

        user_id = get_uid_or_abort_on_bad_token(args['token'])
        rating = db.sqlite.get_itinerary_rating(id)

        if rating.itinerary_id != itinerary_id:
            abort(400, message="rating's itinerary id does not match expected itinerary_id")

        return rating.as_dict()

    def put(self, itinerary_id, id):
        args = self.put_reqparse.parse_args()

        user_id = get_uid_or_abort_on_bad_token(args['token'])
        updated_rating = ItineraryRating(
            id=id,
            itinerary_id=itinerary_id,
            user_id=user_id,
            rating=args['rating']
        )
        db.sqlite.update_itinerary_rating(updated_rating)
        return db.sqlite.get_itinerary_rating(id).as_dict()


class ListRatingResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('token', type=str, required=True, location='args', help='No token to verify')
        super(ListRatingResource, self).__init__()

    def get(self, itinerary_id):
        args = self.reqparse.parse_args()

        get_uid_or_abort_on_bad_token(args['token'])
        ratings = db.sqlite.get_itinerary_rating_list(itinerary_id)
        ratings_dict = [r.as_dict() for r in ratings]
        return ratings_dict


class ListCategoryResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('token', type=str, required=True, location='args', help='No token to verify')
        super(ListCategoryResource, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()

        user_id = get_uid_or_abort_on_bad_token(args['token'])

        categories = [c.as_dict() for c in model.categories]
        return categories, 200


class QueryCategoryResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('token', type=str, required=True, location='args', help='No token to verify')
        self.reqparse.add_argument('term', type=str, required=False, location='args')
        self.reqparse.add_argument('location', type=str, required=True, location='args', help='Need a location to query')
        self.reqparse.add_argument('latitude', type=str, required=False, location='args')
        self.reqparse.add_argument('longitude', type=str, required=False, location='args')

        super(QueryCategoryResource, self).__init__()

    def get(self, category_str):
        args = self.reqparse.parse_args()
        user_id = get_uid_or_abort_on_bad_token(args['token'])

        category = model.match_category(category_str)
        if not args['term']:
            term = category.search_term
        else:
            term = args['term']

        results = yelpapi.search(term, args['location'], category.filters)
        return results, 200


def get_uid_or_abort_on_bad_token(token):
    uid = db.sqlite.check_authorization(token)
    if not uid:
        abort(401, message='Bad token')
    else:
        return uid


def abort_on_invalid_item_relation(item, itinerary_id, user_id):
    itinerary = db.sqlite.get_itinerary(itinerary_id)

    if not itinerary or not item:
        abort(404, message='Item or itinerary not found')

    if itinerary.user.id != user_id:
        abort(401, message='Do not own itinerary')

    #TODO(abettadapur): check itinerary list for the item
    # if item not in itinerary.items:
    #     abort(400, message='Item does not belong to given itinerary id')


def abort_on_invalid_itinerary(itinerary, user_id):
    if not itinerary:
        abort(404, message='Itinerary not found')

    if itinerary.user.id != user_id:
        abort(401, message='Do not own itinerary')
