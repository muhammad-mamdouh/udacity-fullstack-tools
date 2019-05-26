#
# Test script for the Bookmark Server.
#
# The server should be listening on port 8000, answer a GET request to /
# with an HTML document, answer a POST request by testing the provided URI
# and responding accordingly, and answer a GET request to /name depending
# on whether the name was previously stored or not.

import requests, socket

def test_connect():
    '''Try connecting to the server.'''
    print("\nTesting connecting to the server.")
    try:
        with socket.socket() as s:
            s.connect(("localhost", 8000))
        print("Connection attempt succeeded.")
        return None
    except socket.error:
        return "Server didn't answer on localhost port 8000.  Is it running?"

def test_URIChecker_bad():
    '''The URIChecker code should return False for a bad URI.'''
    print("\nTesting URIChecker function for a bad URI.")
    from BookmarkServer import URIChecker
    try:
        bad = URIChecker("this is a bad uri")
    except NotImplementedError:
        return ("URIChecker raised NotImplementedError.")

    if bad is not False:
        return ("URIChecker returned {} on a bad URI instead of False.".format(
            bad))
    else:
        print("URIChecker correctly tested a bad URI.")
        return None

def test_GET_root():
    '''The server should accept a GET and return the form.'''
    print("\nTesting GET request.")
    uri = "http://localhost:8000/"
    try:
        req = requests.get(uri)
    except requests.RequestException as e:
        return ("Couldn't communicate with the server. ({})\n"
                "If it's running, take a look at its output.").format(e)

    if req.status_code == 501:
        return ("The server returned status code 501 Not Implemented.\n"
                "This means it doesn't know how to handle a GET request.\n"
                "(Is the correct server code running?)")
    elif req.status_code != 200:
        return ("The server returned status code {} instead of a 200 OK."
                ).format(req.status_code)
    elif not req.headers['content-type'].lower().startswith('text/html'):
        return ("The server didn't return Content-type: text/html.")
    elif "<title>Bookmark Server</title>" not in req.text:
        return ("The server didn't return the form text I expected.")
    else:
        print("GET request succeeded!")
        return None

def test_URIChecker_good():
    '''The URIChecker code should return True for a good URI.'''
    print("\nTesting URIChecker function for a good URI.")
    from BookmarkServer import URIChecker
    try:
        good = URIChecker("https://www.google.com")
    except NotImplementedError:
        return ("URIChecker raised NotImplementedError.")

    if good is False:
        return ("URIChecker returned {} on a good URI instead of True.\n"
                "(Or maybe Google is down.)".format(good))
    else:
        print("URIChecker correctly tested a good URI.")
        return None

def test_POST_nodata():
    '''The server should accept a POST and return 400 error on empty form.'''
    print("\nTesting POST request with empty form.")

    uri = "http://localhost:8000/"
    data = {}

    try:
        req = requests.post(uri, data=data, allow_redirects=False)
    except requests.ConnectionError as e:
        return ("Server dropped the connection.")

    if req.status_code == 501:
        return ("The server returned status code 501 Not Implemented.\n"
                "This means it doesn't know how to handle a POST request.\n"
                "(Is the correct server code running?)")
    elif req.status_code != 400:
        return ("Server returned status code {} instead of 400 when I gave\n"
                "it an empty form in a POST request.".format(req.status_code))
    else:
        print("POST request with bad URI correctly got a 400.")
        return None


def test_POST_bad():
    '''The server should accept a POST and return 404 error on bad URI.'''
    print("\nTesting POST request with bad URI.")

    uri = "http://localhost:8000/"
    data = {'shortname': 'bad', 'longuri': 'this is fake'}
    try:
        req = requests.post(uri, data=data, allow_redirects=False)
    except requests.ConnectionError as e:
        return ("Server dropped the connection.")

    if req.status_code == 501:
        return ("The server returned status code 501 Not Implemented.\n"
                "This means it doesn't know how to handle a POST request.\n"
                "(Is the correct server code running?)")
    elif req.status_code != 404:
        return ("Server returned status code {} instead of 404 when I gave\n"
                "it a bad URI in a POST request.".format(req.status_code))
    else:
        print("POST request with bad URI correctly got a 404.")
        return None


def test_POST_good():
    '''The server should accept a POST with a good URI and redirect to root.'''
    print("\nTesting POST request with good URI.")

    uri = "http://localhost:8000/"
    data = {'longuri': 'http://www.google.com/', 'shortname': 'google'}
    try:
        req = requests.post(uri, data=data, allow_redirects=False)
    except requests.ConnectionError as e:
        return ("Server dropped the connection.")

    if req.status_code == 501:
        return ("The server returned status code 501 Not Implemented.\n"
                "This means it doesn't know how to handle a POST request.\n"
                "(Is the correct server code running?)")
    elif req.status_code != 303:
        return ("Server returned status code {} instead of 303 when I gave\n"
                "it a good URI in a POST request.".format(req.status_code))
    elif 'location' not in req.headers:
        return ("Server returned a 303 redirect with no Location header.")
    elif req.headers['location'] != '/':
        return ("Server returned redirect to {} instead of to /."
                .format(req.headers['location']))
    else:
        print("POST request with good URI correctly got a 303 to /.")
        return None

def test_GET_path():
    '''The server should redirect on a GET to a recorded URI.'''
    print("\nTesting a recorded URI redirection process.")
    uri = "http://localhost:8000/google"
    orig = "http://www.google.com/"
    print("Testing GET request to {}.".format(uri))

    try:
        req = requests.get(uri, allow_redirects=False)
    except requests.ConnectionError as e:
        return ("Server dropped the connection.")

    if req.status_code == 501:
        return ("The server returned status code 501 Not Implemented.\n"
                "This means it doesn't know how to handle a GET request.\n"
                "(Is the correct server code running?)")
    elif req.status_code != 303:
        return ("Server returned status code {} instead of 303 when I asked\n"
                "for it to follow a short URI.".format(req.status_code))
    elif 'location' not in req.headers:
        return ("Server returned a 303 with no Location header.")
    elif req.headers['Location'] != 'http://www.google.com/':
        return ("Server returned a 303, but with a Location header of {}\n"
                "when I expected it to be http://www.google.com/."
                .format(req.headers['location']))
    else:
        print("GET request to {} returned 303 to {} successfully"
              .format(uri, orig))

if __name__ == "__main__":
    tests = [test_connect, test_GET_root, test_URIChecker_bad, test_URIChecker_good,
             test_POST_nodata, test_POST_bad, test_POST_good, test_GET_path]
    for test in tests:
        error = test()
        if error is not None:
            print(error)
            break
    if not error:
        print("\nAll tests succeeded!")
