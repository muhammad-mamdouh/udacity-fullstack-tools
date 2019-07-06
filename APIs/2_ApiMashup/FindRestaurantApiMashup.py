import urllib.request
import urllib.parse
import urllib.error
import datetime
import json
import ssl
from LocationGeocoding import get_coordinates

FOURSQUARE_CLIENT_ID = "PASTE_CLIENT_ID_HERE"
FOURSQUARE_CLIENT_SECRET = "PASTE_CLIENT_SECRET_HERE"

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def find_restaurant(meal_type, location):
    latitude, longitude = get_coordinates(location)
    current_date = datetime.datetime.now()
    current_date_formatted = current_date.strftime("%Y%m%d")
    params = dict()
    params['v'] = current_date_formatted
    params['ll'] = f'{latitude},{longitude}'
    params['query'] = meal_type

    # Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
    service_uri = f'https://api.foursquare.com/v2/venues/search?client_id={FOURSQUARE_CLIENT_ID}&client_secret={FOURSQUARE_CLIENT_SECRET}&'
    restaurants_uri = service_uri + urllib.parse.urlencode(params)
    restaurants_response = urllib.request.urlopen(restaurants_uri, context=ctx)
    restaurants_response_data = restaurants_response.read().decode()
    restaurants_response_json = json.loads(restaurants_response_data)

    # Grab the first restaurant
    if restaurants_response_json['response']['venues']:
        restaurant = restaurants_response_json['response']['venues'][0]
        venue_id = restaurant['id']
        restaurant_name = restaurant['name']
        restaurant_address_not_formatted = restaurant['location']['formattedAddress']
        restaurant_address_formatted = ' '.join([''.join(line) for line in restaurant_address_not_formatted])

        photos_uri = f'https://api.foursquare.com/v2/venues/{venue_id}/photos?client_id={FOURSQUARE_CLIENT_ID}&v={current_date_formatted}&client_secret={FOURSQUARE_CLIENT_SECRET}'
        photos_response = urllib.request.urlopen(photos_uri, context=ctx)
        photos_response_data = photos_response.read().decode()
        photos_response_json = json.loads(photos_response_data)
        # Grab the first image
        if photos_response_json['response']['photos']['items']:
            first_pic = photos_response_json['response']['photos']['items'][0]
            prefix = first_pic['prefix']
            suffix = first_pic['suffix']
            image_URL = prefix + '300x300' + suffix
        else:
            # If no image available, insert default image url
            image_URL = 'http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct'

        # Return a dictionary containing the restaurant name, address, and image url
        restaurant_dict = {'name': restaurant_name, 'address': restaurant_address_formatted, 'image': image_URL}
        print(f'Restaurant Name: {restaurant_dict["name"]}')
        print(f'Restaurant Address: {restaurant_dict["address"]}')
        print(f'Image: {restaurant_dict["image"]}\n')
        return restaurant_dict
    else:
        # If no restaurants at the entered location
        print(f'No restaurants found at {location}')
        return 'No restaurants to return.'


if __name__ == '__main__':
    find_restaurant('Pizza', 'Tokyo, Japan')
    find_restaurant('Tacos', 'Jakarta, Indonesia')
    find_restaurant('Tapas', 'Maputo, Mozambique')
    find_restaurant('Falafel', 'Cairo, Egypt')
    find_restaurant('Spaghetti', 'New Delhi, India')
    find_restaurant('Cappuccino', 'Geneva, Switzerland')
    find_restaurant('Sushi', 'Los Angeles, California')
    find_restaurant('Steak', 'La Paz, Bolivia')
    find_restaurant('Gyros', 'Sydney, Australia')
