# Instructions:
#
# The starter code for this exercise is the code from the hello server.
# Your assignment is to change this code into the echo server:
#
#   1. Change the name of the handler from EchoHandler to EchoHandler.
#   2. Change the response body from "Hello, HTTP!" to the query path.
#
# When you're done, run it in your terminal.  Try it out from your browser,
# then run the "test.py" script to check your work.

from http.server import HTTPServer, BaseHTTPRequestHandler


class EchoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # First, send a 200 OK response.
        self.send_response(200)

        # Then send headers.
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()

        # Now, write the response body.
		# Echo the request path using path instance variable, [1:] string slice used here to remove the '/'
        self.wfile.write(self.path[1:].encode())

if __name__ == '__main__':
    server_address = ('', 8000)  # Serve on all addresses, port 8000.
    httpd = HTTPServer(server_address, EchoHandler)
    httpd.serve_forever()
