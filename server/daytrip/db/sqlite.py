from pysqlite2 import dbapi2 as sqlite3
import users

class SqlLiteManager(object):

    CREATE_DATABASE = users.CREATE_USERS_TABLE #+ othertable.CREATEOTHERTABLE
    def __init__(self):
        self.conn = sqlite3.connect('temp')
        self.init_db()


    def init_db():
        cursor = self.conn.cursor()
        cursor.execute(CREATE_DATABASE)
        cursor.close()

    def user_exists(self, id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT {id} FROM {table} WHERE {id}=?'.format(id=users.ID, table=users.USERS_TABLE), (id))
        if cursor.rowcount>0:
            cursor.close()
            return True
        else:
            cursor.close()


    def create_user(self, id, first_name, last_name, email):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO {table} ({id},{first_name},{last_name},{email}) VALUES (?,?,?,?)'.format(table=users.USERS_TABLE, id=users.ID, first_name=users.FIRST_NAME, last_name=users.LAST_NAME, email=users.EMAIL), (id, first_name, last_name, email))
        if cursor.rowcount == 0:
            pass #ERROR
        cursor.close()
