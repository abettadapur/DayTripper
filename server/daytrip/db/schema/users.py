ID = 'id'
FIRST_NAME = 'first_name'
LAST_NAME = 'last_name'
EMAIL = 'email_address'
USERS_TABLE = 'users'
CREATE_USERS_TABLE = '''create table if not exists {0}
({1} text primary key, {2} text, {3} text, {4} text);'''.format(USERS_TABLE, ID, FIRST_NAME, LAST_NAME, EMAIL)
