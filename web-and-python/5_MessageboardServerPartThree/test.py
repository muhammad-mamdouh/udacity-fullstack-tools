# Test script for the Messageboard Part Three server.
#
# The server should be listening on port 8000, answer a GET request with
# an HTML document, and answer a POST request with a redirect to the
# main page.

import requests, random, socket

def test_connect():
    '''Try connecting to the server.'''
    print("Testing connecting to the server.")

    try:
        with socket.socket() as s:
           s.connect(("localhost", 8000))
        print("Connection attempt succeeded.")
        return None
    except socket.error:
        return "Server didn't answer on localhost port 8000.  Is it running?"

def test_GET():
    '''The server should accept a GET and return the form.'''
    print("Testing GET request.")
    uri = "http://localhost:8000/"

    try:
        req = requests.get(uri)
    except requests.RequestException as e:
        return ("Couldn't communicate with the server. ({})\n"
                "If it's running, take a look at its output.").format(e)

    if req.status_code==501:
        return ("The server returned status code 501 Not Implemented.\n"
                "This means it doesn't know how to handle a GET request.\n"
                "(Is the correct server code running?)")
    elif req.status_code!=200:
        return ("The server returned status code {} instead of a 200 OK."
                ).format(req.status_code)
    elif not req.headers['content-type'].lower().startswith('text/html'):
        return ("The server didn't return Content-type: text/html.")
    elif '<title>Message Board</title>' not in req.text:
        return ("The server didn't return the form text I expected.")
    else:
        print("GET request succeeded!")
        return None

def test_POST_303():
    '''The server should accept a POST and return a 303 to /.'''
    print("Testing POST request, looking for redirect.")
    msg = random.choice(["Hi there!", "Hello!", "Greetings!"])
    uri = "http://localhost:8000/"

    try:
        req = requests.post(uri, data = {'message': msg}, allow_redirects=False)
    except requests.RequestException as e:
        return ("Couldn't communicate with the server. ({})\n"
                "If it's running, take a look at its output.").format(e)

    if req.status_code == 501:
        return ("The server returned status code 501 Not Implemented.\n"
                "This means it doesn't know how to handle a POST request.\n"
                "(Is the correct server code running?)")
    elif req.status_code != 303:
        return ("The server returned status code {} instead of a 303 redirect."
                ).format(req.status_code)
    elif req.headers['location'] != '/':
        return ("The server sent a 303 redirect to the wrong location."
                "I expected '/' but it sent '{}'.").format(
                    req.headers['location'])
    else:
        print("POST request succeeded.")
        return None

def test_memory():
    '''The server should remember posts.'''
    print("Testing whether messageboard saves messages.")
    uri = "http://localhost:8000"
    msg = random.choice(["Remember me!", "Don't forget.", "You know me."])
    req = requests.post(uri, data = {'message': msg})

    if req.status_code != 200:
        return ("Got status code {} instead of 200 on Post-Redirect-Get."
                ).format(req.status_code)
    elif msg not in req.text:
        return ("I posted a message but it didn't show up.\n"
                "Expected '{}' to appear, but got this output instead:\n"
                "{}").format(msg, req.text)
    else:
        print("Post-Redirect-Get succeeded and I saw my message!")

if __name__ == '__main__':
    tests = [test_connect, test_GET, test_POST_303, test_memory]
    for test in tests:
        problem = test()
        if problem is not None:
            print(problem)
            break
    if not problem:
        print("All tests succeeded!")
