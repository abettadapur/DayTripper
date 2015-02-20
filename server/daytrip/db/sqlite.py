from pysqlite2 import dbapi2 as sqlite3
import users


CREATE_DATABASE = users.CREATE_USERS_TABLE #+ othertable.CREATEOTHERTABLE
class SqlLiteManager(object):


    def __init__(self):
        self.db_name = 'temp'
        self.init_db()


    def init_db(self):
        global CREATE_DATABASE
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(CREATE_DATABASE)
            cursor.close()

    def user_exists(self, id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT {id} FROM {table} WHERE {id}=?'.format(id=users.ID, table=users.USERS_TABLE), (id,))
            if cursor.rowcount>0:
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
