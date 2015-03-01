import users

ID = 'id'
USER_ID = 'user_id'
NAME = 'name'
DATE = 'date'
START_TIME = 'start_time'
END_TIME = 'end_time'
CITY = 'city'
ITINERARY_TABLE = 'itinerary'

CREATE_ITINERARY_TABLE = '''create table if not exists {0}
({1} text primary key, {2} text, {3} text, {4} integer, {5} integer, {6} integer, {7} text, foreign key({2}) REFERENCES {8}({9}));
'''.format(ITINERARY_TABLE, ID, USER_ID, NAME, DATE, START_TIME, END_TIME, CITY, users.USERS_TABLE, users.ID)



