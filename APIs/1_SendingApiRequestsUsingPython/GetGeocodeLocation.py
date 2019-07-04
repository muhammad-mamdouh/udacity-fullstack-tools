import httplib2
import json
import os


with open('/etc/geocodeLocation_config.json') as config_file:
    config = json.load(config_file)

CLIENT_ID = config.get('CLIENT_ID')
CLIENT_SECRET = config.get('CLIENT_SECRET')
GOOGLE_API_KEY = config.get('GOOGLE_API_KEY')


foresquare_search_uri = f'https://api.foursquare.com/v2/venues/search?ll=40.7,-74&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&v=20190704'
foresquare_explore_uri = f'https://api.foursquare.com/v2/venues/explore?cat=food&near=bentonville&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&v=20190704'


def getGeocodeLocation(inputString):
    '''
    Use Google Maps to convert a location into Latitute/Longitute coordinates
    # FORMAT: https://maps.googleapis.com/maps/api/geocode/json?
        address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=API_KEY
    '''
    locationString = inputString.replace(" ", "+")
    google_api_uri = f'https://maps.googleapis.com/maps/api/geocode/json?address={locationString}&key={GOOGLE_API_KEY}'
    h = httplib2.Http()
    response, content = h.request(google_api_uri, 'GET')
    result = json.loads(content)
    print(f'Response header: {response}\n\n')
    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']
    return (latitude, longitude)


location = '1600 Amphitheatre Parkway, Mountain View, CA'
getGeocodeLocation(location)
