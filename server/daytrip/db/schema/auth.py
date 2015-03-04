TOKEN = 'auth_token'
USER_ID = 'user_id'
AUTH_TABLE = "auth_tokens"
CREATE_AUTH_TABLE = '''create table if not exists {0}
({1} text primary key, {2} integer);'''.format(AUTH_TABLE, TOKEN, USER_ID)
