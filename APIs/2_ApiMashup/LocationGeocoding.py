import urllib.request
import urllib.parse
import urllib.error
import json
import ssl

api_key = False

if api_key is False:
    api_key = 'API_KEY'
    serviceuri = 'ANOTHER_PAID_GEOCODE_URI'
else:
    serviceuri = 'https://maps.googleapis.com/maps/api/geocode/json?'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def get_coordinates(location):
    address = location
    if len(address) < 1:
        return False

    params = dict()
    params['address'] = address

    if api_key is not False:
        params['key'] = api_key

    uri = serviceuri + urllib.parse.urlencode(params)

    print('Retrieving', uri)
    response = urllib.request.urlopen(uri, context=ctx)
    data = response.read().decode()
    json_data = json.loads(data)

    latitude, longitude = json_data['results'][0]['geometry']['location'].values()
    return (latitude, longitude)
