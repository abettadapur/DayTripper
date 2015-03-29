from yelp import yelpapi
import model
import db
import codecs


DEFAULT_CITIES = ['Atlanta', 'Seattle', 'Austin', 'Philadelphia', 'Portland', 'Miami']
DEFAULT_CATEGORY_NAMES = ['breakfast', 'lunch', 'dinner', 'attraction', 'nightlife']

LOGGING_ENABLED = True

# loads database with...
#   yelp_entries              ...for each category for each city
#   yelp_locations            ...for each yelp entry
def run(cities=DEFAULT_CITIES, category_names=DEFAULT_CATEGORY_NAMES):
    for city in cities:
        log("Populating database for '" + city + "'...")

        for category_name in category_names:
            cache_yelp_entries(city, category_name)
            log('')


def cache_yelp_entries(city, category_name):
    category = model.match_category(category_name)

    log('\tYelpAPI: Search call for category ' + category_name)
    yelp_api_results = yelpapi.search(category.search_term, city, category.filters)

    log('\tYelpAPI: Making Business calls (and scraping for prices) and caching entries...')
    count = 0
    for api_result in yelp_api_results:
        if not db.sqlite.has_yelp_entry(api_result['id']):
            if len(api_result['location']['address']) > 0:
                log('\t\tcaching <' + api_result['url'] + '>')
                count += 1
                entry = yelpapi.business(api_result['id'])
                db.sqlite.insert_yelp_entry(entry)
            else:
                log('Could not cache: '+str(api_result))
        else:
            log('Already added: '+ api_result['id'])

    log("\t" + str(count) + " new yelp_entries for category '" + category_name + "'")


def log(message):
    if LOGGING_ENABLED:
        with codecs.open('log.txt', 'a', 'utf-8') as file:
            file.write(message + '\n')
        print message


if __name__ == '__main__':
    run()
