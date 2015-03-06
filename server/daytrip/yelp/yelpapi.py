import json
import urllib
import urllib2
import pprint
import oauth2

from etc import config



API_HOST = "api.yelp.com"
SEARCH_PATH = "/v2/search/"
BUSINESS_PATH = '/v2/business/'

CONSUMER_KEY = config.CONSUMER_KEY
CONSUMER_SECRET = config.CONSUMER_SECRET
TOKEN = config.TOKEN
TOKEN_SECRET = config.TOKEN_SECRET


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
    print signed_url

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

    return request(API_HOST, SEARCH_PATH, url_params=url_params)

def business(yelp_id):
    return request(API_HOST, BUSINESS_PATH+yelp_id)



if __name__ == "__main__":
    results = search("", "Atlanta", ['shopping'])
    for business in results['businesses']:
        print business['name']
