import itinerary
import users


ID = 'id'
ITINERARY_ID = 'itinerary_id'
USER_ID = 'user_id'
RATING = 'rating'

ITINERARY_RATING_TABLE = 'itinerary_rating'

CREATE_ITINERARY_RATING_TABLE = '''
create table if not exists {table} (
    {id} integer primary key autoincrement,
    {itinerary_id} integer,
    {user_id} integer,
    {rating} integer,
    foreign key({itinerary_id}) references {itinerary_table}({itinerary_table_id}),
    foreign key({user_id}) references {user_table}({user_table_id})
)
'''.format(
    id=ID,
    table=ITINERARY_RATING_TABLE,
    itinerary_id=ITINERARY_ID,
    user_id=USER_ID,
    rating=RATING,
    itinerary_table=itinerary.ITINERARY_TABLE,
    itinerary_table_id=itinerary.ID,
    user_table=users.USERS_TABLE,
    user_table_id=users.ID
)
