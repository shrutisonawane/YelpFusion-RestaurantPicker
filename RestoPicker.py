_author_="Shruti Sonawane"


# Fall back to Python 2's urllib2 and urllib
from urllib import quote
from urllib import urlencode

# This library helps get co-ordinates for cities
from geopy.geocoders import Nominatim
import random
import requests
import sys


# Fusion app details
CLIENT_ID = "<Your_Client_ID>"
CLIENT_SECRET = "<Your_Client_Secret>"

# API constants
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'

DEFAULT_TERM = 'lunch'
DEFAULT_LOCATION = 'Tempe, AZ'
SEARCH_LIMIT = 10


# Method to make POST request to API to get access token
def obtain_bearer_token(host, path):
    try:
        url = '{0}{1}'.format(host, quote(path.encode('utf8')))
        assert CLIENT_ID, "Please supply your client_id."
        assert CLIENT_SECRET, "Please supply your client_secret."
        data = urlencode({
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': GRANT_TYPE,
        })
        headers = {'content-type': 'application/x-www-form-urlencoded',}
        response = requests.request('POST', url, data=data, headers=headers)
        bearer_token = response.json()['access_token']
        return bearer_token

    except Exception as ex:
        print "Error while getting access token: ",ex


#Method to construct GET request to Yelp API
def request(host, path, bearer_token, url_params=None):
    try:
        url_params = url_params or {}
        url = '{0}{1}'.format(host, quote(path.encode('utf8')))
        headers = {
            'Authorization': 'Bearer %s' % bearer_token,
        }
        print(u'Querying {0} ...'.format(url))
        response = requests.request('GET', url, headers=headers, params=url_params)
        return response.json()

    except Exception as ex:
        print "Error while processing request: ",ex


# Constructs the request
def search(bearer_token, term, location):
    try:
        url_params = {
            'term': term.replace(' ', '+'),
            'location': location.replace(' ', '+'),
            'limit': SEARCH_LIMIT
        }
        return request(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)

    except Exception as ex:
        print ex


def main():
    try:
        print "Welcome to Lunch Time Resto Decider!\nBcoz you are too hungry to decide where to eat...."
        bearer_token = obtain_bearer_token(API_HOST,TOKEN_PATH)
        print "1. Default: Arizona State University, Tempe, AZ"
        print "2. Choose new location"
        usr_input = raw_input("Enter option: ")

        if usr_input=='1':
            resp_json = request(API_HOST,SEARCH_PATH,bearer_token,"latitude=33.423611&longitude=-111.939687")
            list = resp_json['businesses']
            randList =[]
            randAddr = []

            for stuff in list:
                if (stuff['price']=='$' or stuff['price']=='$$') and (str(stuff['rating'])>=4.0):
                    randList.append(stuff['name'])
                    randAddr.append(stuff['location'])
            randomInt = random.randint(0,len(randList)-1)
            randResto = randList[randomInt]
            randAddress = randAddr[randomInt]['display_address']
            print "The random restaurant you should visit today in Tempe is.... ", randResto,"!!"
            print "Address:"
            for place in randAddress:
                print place


        elif usr_input=='2':
            new_loc = raw_input("Enter location: ")
            try:
                geolocator = Nominatim()
                location = geolocator.geocode(new_loc)
                if location is None:
                    print "Are you sure you spelt it right? Please check again."
                    sys.exit(0)

            except Exception as ex:
                pass

            string_params = "latitude="+str(location.latitude)+"&longitude="+str(location.longitude)
            resp_json = request(API_HOST,SEARCH_PATH,bearer_token,string_params)
            list = []
            list = resp_json['businesses']
            randList =[]
            randAddr = []

            for stuff in list:
                if (str(stuff['rating'])>=4.0):
                    randList.append(stuff['name'])
                    randAddr.append(stuff['location'])
            randomInt = random.randint(0,len(randList)-1)
            randResto = randList[randomInt]
            randAddress = randAddr[randomInt]['display_address']
            print "The random restaurant you should visit today in ",new_loc," is.... ", randResto,"!!"
            print "Address:"

            for place in randAddress:
                print place

        else:
            print "Incorrect option chosen"
    except Exception as e:
        print "Oops! Something went wrong. Exiting..:",e

if __name__ == '__main__':
    main()

