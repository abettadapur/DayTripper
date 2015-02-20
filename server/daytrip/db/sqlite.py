from sqlite3 import dbapi2 as sqlite3
from schema import users, auth


#CREATE_DATABASE = users.CREATE_USERS_TABLE + auth.CREATE_AUTH_TABLE #+ othertable.CREATEOTHERTABLE
class SqlLiteManager(object):


    def __init__(self):
        self.db_name = 'temp.db'
        self.init_db()


    def init_db(self):
        global CREATE_DATABASE
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(users.CREATE_USERS_TABLE)
            cursor.execute(auth.CREATE_AUTH_TABLE)
            cursor.close()

    #USERS OPERATIONS
    def user_exists(self, id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT {id} FROM {table} WHERE {id}=?'.format(id=users.ID, table=users.USERS_TABLE), (id,))
            if cursor.fetchone():
                cursor.close()
                return True
            else:
                cursor.close()


    def create_user(self, id, first_name, last_name, email):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO {table} ({id},{first_name},{last_name},{email}) VALUES (?,?,?,?)'.format(table=users.USERS_TABLE, id=users.ID, first_name=users.FIRST_NAME, last_name=users.LAST_NAME, email=users.EMAIL), (id, first_name, last_name, email))
            if cursor.rowcount == 0:
                pass #ERROR
            cursor.close()

    def get_user(self, id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM {table} WHERE {id}=:id'.format(id=users.ID, table=users.USERS_TABLE), (id,))
            user = cursor.fetchone()
            cursor.close()
            return user

    def list_users(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM {table}'.format(table=users.USERS_TABLE))
            users = cursor.fetchall()
            cursor.close()
            return users

    #AUTH OPERATIONS

    def add_authorization(self, token, user_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO {table} ({token}, {user_id}) VALUES(?,?)'.format(table=auth.AUTH_TABLE, token=auth.TOKEN, user_id=auth.USER_ID), (token, user_id))
            if cursor.rowcount==0:
                pass #ERROR
            cursor.close()


    def check_authorization(self, token):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT {token} FROM {table} WHERE {token}=?'.format(token=auth.TOKEN, table=auth.AUTH_TABLE), (token,))
            if cursor.fetchone():
                cursor.close()
                return True
            cursor.close()

    def delete_authorization(self, token):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM {table} WHERE {token}=?'.format(table=auth.AUTH_TABLE, token=auth.TOKEN))
            if cursor.rowcount==0:
                pass #ERROR
            cursor.close()
