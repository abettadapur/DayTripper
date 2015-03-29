import json
import urllib
import urllib2
import pprint
import oauth2
import lxml
from bs4 import BeautifulSoup

from etc import config
from model.yelp_entry import YelpEntry
from model.yelp_location import YelpLocation


API_HOST = "api.yelp.com"
SEARCH_PATH = "/v2/search/"
BUSINESS_PATH = '/v2/business/'

CONSUMER_KEY = config.CONSUMER_KEY
CONSUMER_SECRET = config.CONSUMER_SECRET
TOKEN = config.TOKEN
TOKEN_SECRET = config.TOKEN_SECRET


def append_price(business_api_entry):
    """Appends price of 0 if page has no price-range"""
    url = business_api_entry['url']
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    price_element = soup.find("span", {"class":"business-attribute price-range"})
    if price_element is None:
        print("Price not found")
        business_api_entry['price'] = 0
    else:
        print("Price found: {0}".format(price_element.contents[0]))
        business_api_entry['price'] = len(price_element.contents[0])


def request(host, path, url_params=None):
    url_params = url_params or {}

    url = 'http://{0}{1}?'.format(host, urllib.quote(path.encode("utf8")))
    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
                'oauth_nonce': oauth2.generate_nonce(),
                'oauth_timestamp': oauth2.generate_timestamp(),
                'oauth_token': TOKEN,
                'oauth_consumer_key': CONSUMER_KEY
        }
    )

    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url();

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response


def search(term, location, category_filters, **kwargs):
    url_params = {}
    url_params['term']= term.replace(' ', '+') if term else ""
    url_params['location']=location.replace(' ', '+')

    filter_str = ""
    for i in range(0,len(category_filters)):
        filter_str = filter_str + category_filters[i]
        if i != len(category_filters)-1:
            filter_str = filter_str+','

    url_params['category_filter'] = filter_str
    url_params.update(kwargs)
    url_params['radius_filter'] = 150000
    businesses = request(API_HOST, SEARCH_PATH, url_params=url_params)
    return businesses["businesses"]

def business(yelp_id):
    api_entry = request(API_HOST, BUSINESS_PATH+yelp_id)
    append_price(api_entry)
    location = YelpLocation(api_entry['id'], api_entry['location']['address'][0], api_entry['location']['city'], api_entry['location']['postal_code'], api_entry['location']['state_code'], api_entry['location']['coordinate']['latitude'], api_entry['location']['coordinate']['longitude'])
    entry = YelpEntry(api_entry['id'], api_entry['name'], api_entry.get('phone', ''), api_entry['image_url'], api_entry['url'], api_entry['rating'], api_entry['review_count'], location, api_entry.get('price', 0))
    return entry



if __name__ == "__main__":
    results = search("", "Atlanta", ['shopping'])
    for business in results['businesses']:
        print business['name']
