#!/usr/bin/env python3
#

"""
This is a data driven web application that handles GET and POST
requests from a client using the restaurantmenu.db database
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote, parse_qs
import RestaurantsCRUDs

edit_restaurant = "<a href='/restaurant/{}/edit'>Edit<a> | "
delete_restaurant = "<a href='/restaurant/{}/delete'>Delete<a><br><hr>"
create_restaurant = "<a href='/restaurant/new'>Make a New Restaurant Here</a>"

create_restaurant_form = '''
<!DOCTYPE html>
    <title>New Restaurant</title>
    <h1>Create a New Restaurant</h1>
    <form method="POST">
        <label>Restaurant Name: 
            <input name="new_rest_name">
        </label>
        <button type="submit">Create</button>
    </form>
</html>
'''

edit_restaurant_form = '''
<!DOCTYPE html>
    <title>Rename Restaurant</title>
    <h1>Rename Restaurant</h1>
    <h2>{}</h2>
    <form method="POST">
        <label>Restaurant New Name: 
            <input name="edited_rest_name">
        </label>
        <button type="submit">Edit</button>
    </form>
</html>
'''

delete_restaurant_form = '''
<!DOCTYPE html>
    <title>Delete Restaurant</title>
    <h1>Are you sure you want to delete {}?</h1>
    <form method="POST">
        <button type="submit" >Delete</button>
    </form>
</html>
'''


class WebServerHandler(BaseHTTPRequestHandler):
    def redirect_to(self, path):
        self.send_response(301)
        self.send_header('Location', path)
        self.end_headers()

    def get_request_data(self):
        length = int(self.headers.get("Content-length", 0))
        data = self.rfile.read(length).decode()
        return parse_qs(data)

    def check_user_submitted_formfield(self, form_field, data_params):
        if form_field not in data_params:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("Missing form fields!".encode())
            return
        else:
            return True

    def do_POST(self):
        '''Handles all POST requests our web server receives'''
        resource_path = unquote(self.path[1:])
        try:
            # localhost:port/restaurant/new path for creating a new restaurant
            if resource_path == "restaurant/new":
                params = self.get_request_data()
                # User submitted the form?
                if self.check_user_submitted_formfield("new_rest_name", params):
                    rest_name = params["new_rest_name"][0]
                    if RestaurantsCRUDs.create_new_restaurant(rest_name):
                        self.redirect_to('/restaurants')

            # localhost:port/restaurant/restaurant_id/edit path
            # for editing a specific restaurant
            elif self.path.endswith("/edit"):
                params = self.get_request_data()
                # User submitted the form?
                if self.check_user_submitted_formfield("edited_rest_name", params):
                    edited_rest_name = params["edited_rest_name"][0]
                    resource_id_path = self.path.split("/")[2]
                    if RestaurantsCRUDs.edit_restaurant_name(resource_id_path, edited_rest_name):
                        self.redirect_to('/restaurants')

            # localhost:port/restaurant/restaurant_id/delete path
            # for deleting a restaurant record
            elif self.path.endswith("/delete"):
                resource_id_path = self.path.split("/")[2]
                if RestaurantsCRUDs.delete_restaurant(resource_id_path):
                    self.redirect_to('/restaurants')
        except IOError:
            self.send_error(404, "File Not Found {}".format(self.path))

    def do_GET(self):
        '''Handles all GET requests our web server receives'''

        # A GET request will either be for / (the root path) or for /some-name.
        # Strip off the / and we have either empty string or a name.
        resource_path = unquote(self.path[1:])
        try:
            if resource_path:
                # localhost:port/restaurants path for displaying all restaurants
                if resource_path == "restaurants":
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    restaurants_names = RestaurantsCRUDs.get_all_restaurants()
                    output = create_restaurant
                    output += "<h2>Restaurants Existed</h2>"
                    for restaurant in restaurants_names:
                        output += restaurant
                        output += "<br>"
                        output += edit_restaurant.format(
                            RestaurantsCRUDs.get_restaurant_id_by_name(restaurant))
                        output += delete_restaurant.format(
                            RestaurantsCRUDs.get_restaurant_id_by_name(restaurant))
                    self.wfile.write(output.encode())

                elif resource_path == "restaurant/new":
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    output = create_restaurant_form
                    self.wfile.write(output.encode())

                elif self.path.endswith("/edit"):
                    resource_id_path = self.path.split("/")[2]
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    output = edit_restaurant_form
                    rest_name = RestaurantsCRUDs.get_restaurant_name_by_id(resource_id_path)
                    self.wfile.write(output.format(rest_name).encode())

                elif self.path.endswith("/delete"):
                    resource_id_path = self.path.split("/")[2]
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    output = delete_restaurant_form
                    rest_name = RestaurantsCRUDs.get_restaurant_name_by_id(resource_id_path)
                    self.wfile.write(output.format(rest_name).encode())
                else:
                    # We don't know that resource name! Send a 404 error.
                    self.send_response(404)
                    self.send_header('Content-type', 'text/plain; charset=utf-8')
                    self.end_headers()
                    self.wfile.write("I don't know '{}'.".format(resource_path).encode())
            else:   # Empty path, it has to be the root path redirect to all restaurants path
                self.send_response(301)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.send_header('Location', '/restaurants')
                self.end_headers()

        except IOError:
            self.send_error(404, "File Not Found {}".format(self.path))


def main():
    '''
    Instantiate our handler class and specify what port
    it'll listen on.
    return: a server that constantly running -listening- until Ctrl+C hit
    '''
    try:
        port = 8000
        server_address = ('', port)
        server = HTTPServer(server_address, WebServerHandler)
        print("My web server running on port {}".format(port))
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping the web server...")
        server.socket.close()


if __name__ == '__main__':
    main()
