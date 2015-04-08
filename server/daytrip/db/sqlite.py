import json
from sqlite3 import dbapi2 as sqlite3
from schema import users as user_schema, auth as auth_schema, itinerary as itinerary_schema, item as item_schema, yelp_entry, yelp_location, itinerary_rating as itinerary_rating_schema
import datetime
from model.user import User
from model.itinerary import Itinerary
from model.item import Item
from model.yelp_entry import YelpEntry
from model.yelp_location import YelpLocation
from model.itinerary_rating import ItineraryRating
from yelp import yelpapi

#CREATE_DATABASE = users.CREATE_USERS_TABLE + auth.CREATE_AUTH_TABLE #+ othertable.CREATEOTHERTABLE
class SqlLiteManager(object):


    def __init__(self):
        self.db_name = 'temp.db'
        self.init_db()


    def init_db(self):
        global CREATE_DATABASE
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(user_schema.CREATE_USERS_TABLE)
            cursor.execute(auth_schema.CREATE_AUTH_TABLE)
            cursor.execute(itinerary_schema.CREATE_ITINERARY_TABLE)
            cursor.execute(item_schema.CREATE_ITEM_TABLE)
            cursor.execute(yelp_entry.CREATE_YELP_ENTRY_TABLE)
            cursor.execute(yelp_location.CREATE_YELP_LOCATION_TABLE)
            cursor.execute(itinerary_rating_schema.CREATE_ITINERARY_RATING_TABLE)
            cursor.close()

    #USERS OPERATIONS
    def user_exists(self, id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT {id} FROM {table} WHERE {id}=?'.format(
                id=user_schema.ID,
                table=user_schema.USERS_TABLE),
                (id,)
            )
            if cursor.fetchone():
                cursor.close()
                return True
            else:
                cursor.close()

    def insert_user(self, user):
        with sqlite3.connect(self.db_name) as conn:

            cursor = conn.cursor()

            cursor.execute('INSERT INTO {table} ({id},{first_name},{last_name},{email}) VALUES (?,?,?,?)'.format(
                table=user_schema.USERS_TABLE,
                id=user_schema.ID,
                first_name=user_schema.FIRST_NAME,
                last_name=user_schema.LAST_NAME,
                email=user_schema.EMAIL),
                (user.id, user.first_name, user.last_name, user.email)
            )

            if cursor.rowcount == 0:
                pass #ERROR
            cursor.close()

    def get_user(self, user_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.row_factory = self.user_from_cursor
            cursor.execute('SELECT * FROM {table} WHERE {id}=?'.format(
                id=user_schema.ID,
                table=user_schema.USERS_TABLE),
                (user_id,)
            )

            user = cursor.fetchone()
            cursor.close()
            return user

    def list_users(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.row_factory = self.user_from_cursor
            cursor.execute('SELECT * FROM {table}'.format(table=user_schema.USERS_TABLE))
            users = cursor.fetchall()
            cursor.close()
            return users

    def user_from_cursor(self, cursor, row):
        if row:
            user = User(row[0], row[1], row[2], row[3])
            return user
        return None

    #AUTH OPERATIONS

    def insert_authorization(self, token, user_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO {table} ({token}, {user_id}) VALUES(?,?)'.format(
                table=auth_schema.AUTH_TABLE,
                token=auth_schema.TOKEN,
                user_id=auth_schema.USER_ID),
                (token, user_id)
            )

            if cursor.rowcount==0:
                pass #ERROR
            cursor.close()


    def check_authorization(self, token):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT {user_id} FROM {table} WHERE {token}=?'.format(
                user_id=auth_schema.USER_ID,
                token=auth_schema.TOKEN,
                table=auth_schema.AUTH_TABLE), (
                token,)
            )
            uid_row = cursor.fetchone()
            cursor.close()
            if uid_row:
                return uid_row[0]

            return None

    def delete_authorization(self, token):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM {table} WHERE {token}=?'.format(
                table=auth_schema.AUTH_TABLE,
                token=auth_schema.TOKEN)
            )
            if cursor.rowcount==0:
                pass #ERROR
            cursor.close()

    #ITINERARY OPERATIONS
    def insert_itinerary(self, itinerary):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO {table} ({user}, {name}, {date}, {start_time}, {end_time}, {city}, {public}) VALUES (?,?,?,?,?,?,?)'
                .format(
                    table = itinerary_schema.ITINERARY_TABLE,
                    user = itinerary_schema.USER_ID,
                    name = itinerary_schema.NAME,
                    date = itinerary_schema.DATE,
                    start_time = itinerary_schema.START_TIME,
                    end_time = itinerary_schema.END_TIME,
                    city = itinerary_schema.CITY,
                    public = itinerary_schema.PUBLIC
                ),
                (itinerary.user.id, itinerary.name, itinerary.date, itinerary.start_time, itinerary.end_time, itinerary.city, itinerary.public)
            )
            itinerary_id = cursor.lastrowid
            itinerary.id = itinerary_id
            cursor.close()

        for item in itinerary.items:
            self.insert_item(item, itinerary)

        return itinerary_id

    def get_itinerary(self, id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.row_factory = self.itinerary_from_cursor

            cursor.execute(
                'SELECT * FROM {itinerary} WHERE {id} = ?'
                .format(
                    itinerary = itinerary_schema.ITINERARY_TABLE,
                    id = itinerary_schema.ID
                ),
                (id, )
            )

            itinerary = cursor.fetchone()
            cursor.close()
            return itinerary

    def list_itineraries(self, user_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.row_factory = self.itinerary_from_cursor

            cursor.execute(
                'SELECT * FROM {itinerary} WHERE {user_id} = ?'
                .format(
                    itinerary = itinerary_schema.ITINERARY_TABLE,
                    user_id = itinerary_schema.USER_ID
                ),
                (user_id, )
            )

            itineraries = cursor.fetchall()
            cursor.close()
            return itineraries

    def search_itineraries(self, query, city):
        with sqlite3.connect(self.db_name) as conn:
            if not city:
                city = ''
            cursor = conn.cursor()
            cursor.row_factory = self.itinerary_from_cursor
            cursor.execute(
                'SELECT * FROM {table} WHERE {name} LIKE ? AND {city} LIKE ? AND {public} = ?'
                .format(
                    table = itinerary_schema.ITINERARY_TABLE,
                    name = itinerary_schema.NAME,
                    city = itinerary_schema.CITY,
                    public = itinerary_schema.PUBLIC,
                ),
                ('%'+query+'%', '%'+city+'%', True)
            )

            itineraries = cursor.fetchall()
            cursor.close()
            return itineraries

    def update_itinerary(self, itinerary):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE {table} SET {user}=?, {name}=?, {date}=?, {start_time}=?, {end_time}=?, {city}=?, {public}=? WHERE {id}=?'
                .format(
                    table=itinerary_schema.ITINERARY_TABLE,
                    user=itinerary_schema.USER_ID,
                    name=itinerary_schema.NAME,
                    date=itinerary_schema.DATE,
                    start_time=itinerary_schema.START_TIME,
                    end_time=itinerary_schema.END_TIME,
                    city=itinerary_schema.CITY,
                    public = itinerary_schema.PUBLIC,
                    id=itinerary_schema.ID
                ),
                (itinerary.user.id, itinerary.name, itinerary.date, itinerary.start_time, itinerary.end_time, itinerary.city, itinerary.public, itinerary.id)
            )
            cursor.close()

        for item in itinerary.items:
            if not self.item_exists(item):
                self.insert_item(item, itinerary)


    def delete_itinerary(self, id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'DELETE FROM {table} WHERE {id}=?'
                .format(
                    table=itinerary_schema.ITINERARY_TABLE,
                    id=itinerary_schema.ID
                ),
                (id, )
            )
            cursor.close()

    def itinerary_from_cursor(self, cursor, row):
        if row:
            items = self.list_items(row[0])
            user = self.get_user(row[1])
            itinerary = Itinerary(row[0], user, row[2], row[3], row[4], row[5], row[6], row[7]==1, items)
            return itinerary
        return None


    #ITEMS FUNCTIONS

    def insert_item(self, item, itinerary):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO {table} ({name}, {itinerary_id}, {yelp_id}, {category}, {start_time}, {end_time})'
                'VALUES (?,?,?,?,?,?)'
                .format(
                    table = item_schema.ITEM_TABLE,
                    name = item_schema.NAME,
                    itinerary_id=item_schema.ITINERARY_ID,
                    yelp_id = item_schema.YELP_ID,
                    category = item_schema.CATEGORY,
                    start_time = item_schema.START_TIME,
                    end_time = item_schema.END_TIME
                ),
                (item.name, itinerary.id, item.yelp_id, item.category, item.start_time, item.end_time)
            )
            item_id = cursor.lastrowid
            cursor.close()

        item.yelp_entry = self.get_yelp_entry(item.yelp_id)
        return item_id

    def item_exists(self, item):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT {id} from {table} WHERE {id}=?'
                .format(table=item_schema.ITEM_TABLE, id=item_schema.ID)
                , (item.id, )
            )

            item = cursor.fetchone()
            cursor.close()
            if item:
                return True
            return False

    def get_item(self, id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.row_factory = self.item_from_cursor

            cursor.execute(
                'SELECT * FROM {table} WHERE {id} = ?'
                .format(
                    table=item_schema.ITEM_TABLE,
                    id=item_schema.ID
                ),
                (id, )
            )

            item = cursor.fetchone()
            cursor.close()
            return item

    def list_items(self, itinerary_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.row_factory = self.item_from_cursor

            cursor.execute(
                'SELECT * FROM {table} WHERE {itinerary_id} = ?'
                .format(
                    table = item_schema.ITEM_TABLE,
                    itinerary_id = item_schema.ITINERARY_ID
                ),
                (itinerary_id,)
            )

            items = cursor.fetchall()
            cursor.close()
            return items

    def update_item(self, item, itinerary_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE {table} SET {name}=?, {itinerary_id}=?, {yelp_id}=?, {category}=?, {start_time}=?, {end_time}=?'
                ' WHERE {id}=?'
                .format(
                    table=item_schema.ITEM_TABLE,
                    name=item_schema.NAME,
                    itinerary_id=item_schema.ITINERARY_ID,
                    yelp_id=item_schema.YELP_ID,
                    category=item_schema.CATEGORY,
                    start_time=item_schema.START_TIME,
                    end_time=item_schema.END_TIME,
                    id=item_schema.ID
                ),
                (item.name, itinerary_id, item.yelp_id, item.category, item.start_time, item.end_time, item.id)
            )
            cursor.close()

    def delete_item(self, id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'DELETE FROM {table} WHERE {id}=?'
                .format(
                    table=item_schema.ITEM_TABLE,
                    id=item_schema.ID
                ),
                (id, )
            )
            cursor.close()

    def item_from_cursor(self, cursor, row):
        if row:
            item = Item(row[0], row[2], row[3], row[4], row[5], row[6])
            item.yelp_entry = self.get_yelp_entry(item.yelp_id)
            return item
        return None

    def get_yelp_count_in_items(self, yelp_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT COUNT(*) FROM {table} WHERE {yelp_id}=?'
                .format(
                    table=item_schema.ITEM_TABLE,
                    yelp_id=item_schema.YELP_ID
                ),
                (yelp_id, )
            )
            row = cursor.fetchone()
            count = row[0]

            cursor.close()
            return count

    # YELP_ENTRY OPERATIONS
    def get_yelp_entry(self, id):
        if not self.has_yelp_entry(id):
            entry = yelpapi.business(id)
            self.insert_yelp_entry(entry)

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.row_factory = self.yelp_entry_from_cursor
            cursor.execute(
                'SELECT * FROM {table} WHERE {id}=?'
                .format(
                    table=yelp_entry.YELP_ENTRY_TABLE,
                    id=yelp_entry.ID
                ),
                (id, )
            )
            entry = cursor.fetchone()
            cursor.close()
            return entry

    def has_yelp_entry(self,id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT {id} FROM {table} WHERE {id}=?'
                .format(
                    table=yelp_entry.YELP_ENTRY_TABLE,
                    id=yelp_entry.ID
                ),
                (id, )
            )
            row = cursor.fetchone()
            cursor.close()
            return row != None


    def insert_yelp_entry(self, entry):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO {table} ({id}, {phone}, {image_url}, {url}, {name}, {rating}, {review_count}, {price})'
                'VALUES (?, ?, ?, ?, ? ,?, ?, ?)'
                .format(
                    table=yelp_entry.YELP_ENTRY_TABLE,
                    id=yelp_entry.ID,
                    phone=yelp_entry.PHONE,
                    image_url=yelp_entry.IMAGE_URL,
                    url=yelp_entry.URL,
                    name=yelp_entry.NAME,
                    rating=yelp_entry.RATING,
                    review_count = yelp_entry.REVIEW_COUNT,
                    price = yelp_entry.PRICE
                ),
                (entry.id, entry.phone, entry.image_url, entry.url, entry.name, entry.rating, entry.review_count, entry.price)
            )

            cursor.close()
        self.insert_yelp_location(entry)


    def yelp_entry_from_cursor(self, cursor, row):
        if row:
            location = self.get_yelp_location(row[0])
            entry = YelpEntry(row[0], row[4], row[1], row[2], row[3], row[5], row[6], location, row[7])
            return entry
        return None


    #YELP_LOCATION_OPERATIONS

    def get_yelp_location(self, yelp_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.row_factory = self.yelp_location_from_cursor
            cursor.execute(
                'SELECT * FROM {table} WHERE {yelp_id} = ?'
                .format(
                    table = yelp_location.YELP_LOCATION_TABLE,
                    yelp_id = yelp_location.YELP_ID
                ),
                (yelp_id, )
            )

            location = cursor.fetchone()
            cursor.close()
            return location

    def insert_yelp_location(self, entry):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            location = entry.location
            cursor.execute(
                'INSERT INTO {table}'
                '({yelp_id}, {address}, {city}, {zip}, {state}, {latitude}, {longitude})'
                'VALUES (?,?,?,?,?,?,?)'
                .format(
                    table = yelp_location.YELP_LOCATION_TABLE,
                    yelp_id = yelp_location.YELP_ID,
                    address = yelp_location.ADDRESS,
                    city = yelp_location.CITY,
                    zip = yelp_location.ZIP,
                    state = yelp_location.STATE,
                    latitude = yelp_location.LATITUDE,
                    longitude = yelp_location.LONGITUDE
                ),
                (location.yelp_id, location.address, location.city, location.postal_code, location.state_code, location.latitude, location.longitude)
            )

            cursor.close()

    def yelp_location_from_cursor(self, cursor, row):
        if row:
            location = YelpLocation(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            return location
        return None

    # ITINERARY RATING OPERATIONS

    def update_itinerary_rating(self, itinerary_rating):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE {rating_table}'
                ' SET {rating}=?'
                ' WHERE {id}=?'
                .format(
                    rating_table=itinerary_rating_schema.ITINERARY_RATING_TABLE,
                    id=itinerary_rating_schema.ID,
                    rating=itinerary_rating_schema.RATING
                ),
                (itinerary_rating.rating, itinerary_rating.id)
            )

            cursor.close()

    def insert_itinerary_rating(self, itinerary_id, user_id, rating):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO {rating_table}'
                ' ({itinerary_id}, {user_id}, {rating})'
                ' VALUES (?,?,?)'
                .format(
                    rating_table=itinerary_rating_schema.ITINERARY_RATING_TABLE,
                    itinerary_id=itinerary_rating_schema.ITINERARY_ID,
                    user_id=itinerary_rating_schema.USER_ID,
                    rating=itinerary_rating_schema.RATING
                ),
                (itinerary_id, user_id, rating)
            )
            rating_id = cursor.lastrowid
            cursor.close()
            return rating_id

    def get_itinerary_rating_list(self, itinerary_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.row_factory = self.itinerary_rating_from_cursor
            cursor.execute(
                'SELECT * FROM {rating_table} WHERE {itinerary_id} = ?'
                .format(
                    rating_table=itinerary_rating_schema.ITINERARY_RATING_TABLE,
                    itinerary_id=itinerary_rating_schema.ITINERARY_ID
                ),
                (itinerary_id,)
            )
            itinerary_ratings = cursor.fetchall()
            cursor.close()
            return itinerary_ratings

    def get_itinerary_rating(self, id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.row_factory = self.itinerary_rating_from_cursor
            cursor.execute(
                'SELECT * FROM {rating_table} WHERE {id}=?'
                .format(
                    rating_table=itinerary_rating_schema.ITINERARY_RATING_TABLE,
                    id=itinerary_rating_schema.ID
                ),
                (id,)
            )
            rating = cursor.fetchone()
            cursor.close()
            return rating


    def itinerary_rating_from_cursor(self, cursor, row):
        if row:
            return ItineraryRating(row[0], row[1], row[2], row[3])
        return None
