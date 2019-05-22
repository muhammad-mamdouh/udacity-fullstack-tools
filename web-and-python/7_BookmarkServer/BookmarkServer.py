from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, unquote
import requests

url_list = {}

form = '''<!DOCTYPE html>
<title>Bookmark Server</title>
<form method="POST">
    <label>Long URI:
        <input name="longuri">
    </label>
    <br>
    <label>Short name:
        <input name="shortname">
    </label>
    <br>
    <button type="submit">Save it!</button>
</form>
<p>URIs I know about:
<pre>
{}
</pre>
'''

def URIChecker(uri, timeout=5):
    '''Check whether this URI is reachable, i.e. does it return a 200 OK?

    This function returns True if a GET request to uri returns a 200 OK, and
    False if that GET request returns any other response, or doesn't return
    (i.e. times out).
    '''
    try:
        req = requests.get(uri, timeout=timeout)
        # If the GET request returns, was it a 200 OK?
        return req.status_code == 200

    except requests.RequestException as e:
        # If the GET request raised an exception, it's not OK.
        return False


class Shortener(BaseHTTPRequestHandler):
    def do_GET(self):
        # A GET request will either be for / (the root path) or for /some-name.
        # Strip off the / and we have either empty string or a name.
        name = unquote(self.path[1:]) # Slice string to ommit /

        if name:
            if name in url_list:
                # We know that name! Send a redirect to it.
                self.send_response(303)
                self.send_header('Location', url_list[name])
                self.end_headers()
            else:
                # We don't know that name! Send a 404 error.
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write("I don't know {}".format(name).encode())
        else:
            # Root path. Send the form.
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            # List the known associations in the form.
            known = "\n".join([key+" : "+url_list[key] for key in url_list.keys()])
            self.wfile.write(form.format(known).encode())

    def do_POST(self):
        # Decode the form data.
        params_length = int(self.headers.get('Content-length', 0))
        body = self.rfile.read(params_length).decode()
        params = parse_qs(body)

        # Check that the user submitted the form fields.
        if "longuri" not in params or "shortname" not in params:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("Missing form fields!".encode())
            return

        long_uri, short_name = [value[0] for value in params.values()]

        # Check if URI is good?
        if URIChecker(long_uri):
            # Store it in url_list dictionary
            url_list[short_name] = long_uri

            # Serve a redirect to the form.
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            # Didn't successfully fetch the long URI.
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("Couldn't fetch URI '{}'. Sorry!".format(long_uri).encode())

if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, Shortener)
    httpd.serve_forever()