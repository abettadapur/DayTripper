import json
from sqlite3 import dbapi2 as sqlite3
from schema import users as user_schema, auth as auth_schema, itinerary as itinerary_schema, item as item_schema
import datetime
from model.user import User
from model.itinerary import Itinerary
from model.item import Item


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

    def get_user(self, id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.row_factory = self.user_from_cursor
            cursor.execute('SELECT * FROM {table} WHERE {id}=?'.format(
                id=user_schema.ID,
                table=user_schema.USERS_TABLE),
                (id,)
            )

            user = cursor.fetchone()
            print str(user)
            cursor.close()
            return user

    def list_users(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM {table}'.format(table=user_schema.USERS_TABLE))
            users = []
            while True:
                user = self.user_from_cursor(cursor)
                if user:
                    users.append(user)
                else:
                    break

            return users

    def user_from_cursor(self, cursor, row):
        print row
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
            uid = cursor.fetchone()
            cursor.close()
            return uid

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
                'INSERT INTO {table} ({user}, {name}, {date}, {start_time}, {end_time}, {city}) VALUES (?,?,?,?,?,?)'
                .format(
                    table = itinerary_schema.ITINERARY_TABLE,
                    user = itinerary_schema.USER_ID,
                    name = itinerary_schema.NAME,
                    date = itinerary_schema.DATE,
                    start_time = itinerary_schema.START_TIME,
                    end_time = itinerary_schema.END_TIME,
                    city = itinerary_schema.CITY
                ),
                (itinerary.user.id, itinerary.name, itinerary.date, itinerary.start_time, itinerary.end_time, itinerary.city)
            )
            if cursor.rowcount==0:
                pass #ERROR
            if len(itinerary.items)> 0:
                pass #CALL INSERT for each item

            cursor.close()

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

    def update_itinerary(self, itinerary):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE {table} SET {user}=?, {name}=?, {date}=?, {start_time}=?, {end_time}=?, {city}=?) WHERE {id}=?'
                .format(
                    table=itinerary_schema.ITINERARY_TABLE,
                    user=itinerary_schema.USER_ID,
                    name=itinerary_schema.NAME,
                    date=itinerary_schema.DATE,
                    start_time=itinerary_schema.START_TIME,
                    end_time=itinerary_schema.END_TIME,
                    city=itinerary_schema.CITY,
                    id=itinerary_schema.ID
                ),
                (itinerary.user.id, itinerary.name, itinerary.date, itinerary.start_time, itinerary.end_time, itinerary.city, itinerary.id)
            )
            cursor.close()

    def delete_itinerary(self, id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'DELETE FROM {table} WHERE {id}=?'
                .format(
                    table=itinerary_schema.ITINERARY_TABLE
                ),
                (id, )
            )
            cursor.close()

    def itinerary_from_cursor(self, cursor, row):
        if row:
            items = self.list_items(row[0])
            user = self.get_user(row[1])
            itinerary = Itinerary(row[0], user, row[2], row[3], row[4], row[5], row[6], items)
            return itinerary
        return None


    #ITEMS FUNCTIONS

    def insert_item(self, item, itinerary):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO {table} ({name}, {itinerary_id}, {yelp_id}, {category_id}, {start_time}, {end_time})'
                'VALUES (?,?,?,?,?,?)'
                .format(
                    table = item_schema.ITEM_TABLE,
                    name = item_schema.NAME,
                    itinerary_id=item_schema.ITINERARY_ID,
                    yelp_id = item_schema.YELP_ID,
                    category_id = item_schema.CATEGORY_ID,
                    start_time = item_schema.START_TIME,
                    end_time = item_schema.END_TIME
                ),
                (item.name, itinerary.id, item.yelp_id, item.category.id, item.start_time, item.end_time)
            )
            if cursor.rowcount == 0:
                pass #ERROR
            cursor.close()

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

    def update_item(self, item, itinerary):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE {table} SET {name}=?, {itinerary_id}=?, {yelp_id}=?, {category_id}=?, {start_time}=?, {end_time}=?)'
                'WHERE {id}=?'
                .format(
                    table=item_schema.ITEM_TABLE,
                    name=item_schema.NAME,
                    itinerary_id=item_schema.ITINERARY_ID,
                    yelp_id=item_schema.YELP_ID,
                    category_id=item_schema.CATEGORY_ID,
                    start_time=item_schema.START_TIME,
                    end_time=item_schema.END_TIME
                ),
                (item.name, itinerary.id, item.yelp_id, item.category.id, item.start_time, item.end_time, item.id)
            )
            cursor.close()

    def delete_item(self, id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'DELETE FROM {table} WHERE {id}=?'
                .format(
                    table=item_schema.ITEM_TABLE
                ),
                (id, )
            )
            cursor.close()

    def item_from_cursor(self, cursor, row):
        if row:
            item = Item(row[0], row[2], row[3], row[4], row[5], row[6])
            return item
        return None





